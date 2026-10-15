"""
Fine-Tuning — 07: LLM Training Internals
========================================
Topics: the six-stage training step, mixed-precision VRAM budgets, and the
misconfiguration findings TRN001-TRN008 that stop a run before it burns a
GPU-hour.

Why this matters:
    A training step is six ordered stages and every hyperparameter maps to
    one of them. This exercise validates a run config — effective batch,
    precision, learning-rate band, warmup, prompt masking, memory, splits,
    and checkpoint metric — and budgets mixed-precision VRAM before launch.

Run:      python 07-training-internals.py
Verify:   python 07-training-internals.py
Validate a real config:
    python 07-training-internals.py path/to/train-config.json
        (exit 0 = no critical findings, 1 = critical findings,
         2 = unreadable file or invalid JSON)

Standard library only. No torch, no network, no API keys.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field, fields
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------

# Bytes per parameter by storage dtype. 1e9 params at N bytes = N GB, so a
# param count in billions multiplied by these values is already in GB.
WEIGHT_BYTES: dict[str, float] = {
    "fp32": 4.0,
    "fp16": 2.0,
    "bf16": 2.0,
    "int8": 1.0,
    "int4": 0.5,
}

# Sane peak-LR bands from the lecture: full fine-tuning moves every weight,
# so the safe learning rate is small; LoRA moves a tiny subspace and needs
# (and tolerates) a higher one.
LR_BANDS: dict[str, tuple[float, float]] = {
    "full": (5e-6, 1e-4),
    "lora": (5e-5, 1e-3),
    "qlora": (5e-5, 1e-3),
}

# Mixed-precision accounting per trainable parameter: gradients stored in
# fp16, AdamW keeping two fp32 moments (the "2x params" of optimizer state,
# 2 tensors x 4 bytes = 8 bytes), and an fp32 master weight copy.
GRAD_BYTES = 2.0
MOMENT_BYTES = 8.0
MASTER_BYTES = 4.0

# Activation heuristic: one fp16 activation per hidden unit per token per
# layer. Without gradient checkpointing, roughly six live temporaries per
# layer; with it, only the layer boundary survives and the rest is
# recomputed during backward.
ACTIVATION_BYTES = 2.0
ACTIVATION_TENSORS = {"checkpointing": 1.0, "full": 6.0}
OVERHEAD_GB = 1.0  # CUDA context, cuDNN workspace, fragmentation slack


@dataclass
class TrainConfig:
    """One training-run configuration, as it would appear in a run file."""

    name: str = "unnamed"
    method: str = "lora"  # "full" | "lora" | "qlora"
    base_params_b: float = 7.0  # base-model size in billions of parameters
    weight_dtype: str = "fp16"  # storage dtype of the (possibly frozen) weights
    trainable_frac: float = 1.0  # fraction of parameters that receive gradients
    optimizer: str = "adamw"  # "adamw" | "sgd"
    precision: str = "fp16"  # autocast compute dtype
    compute_capability: str = "sm_75"  # this workstation: Turing RTX 5000
    allow_precision_fallback: bool = False
    loss_scaler: bool = True  # fp16 needs GradScaler; bf16 does not
    micro_batch: int = 1
    accumulation_steps: int = 1
    grad_parallelism: int = 1  # data-parallel world size
    reported_effective_batch: int | None = None  # what the run config claims
    max_seq_len: int = 2048
    gradient_checkpointing: bool = False
    hidden_size: int = 4096
    num_layers: int = 32
    peak_lr: float | None = None
    warmup_ratio: float | None = None
    lr_schedule: str = "cosine"  # "cosine" | "linear"
    total_steps: int = 1000
    prompt_masking: bool = False  # SFT must mask prompt tokens with -100
    train_path: str | None = None
    eval_path: str | None = None  # must be distinct from train_path
    checkpoint_metric: str | None = None  # held-out, never train loss
    vram_budget_gb: float = 16.0  # this workstation's card

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> TrainConfig:
        """Build a config from a JSON object; unknown keys are ignored."""
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})  # type: ignore[arg-type]


@dataclass
class Finding:
    """A single misconfiguration record.

    `line` names the config field (or JSON key) the finding points at.
    """

    severity: str  # "critical" | "warning"
    code: str  # TRN001..TRN008
    line: str
    message: str


@dataclass(frozen=True)
class VramBreakdown:
    """Mixed-precision training-state estimate, one row per memory term."""

    weights_gb: float
    gradients_gb: float
    optimizer_gb: float
    master_gb: float
    activations_gb: float
    overhead_gb: float

    @property
    def total_gb(self) -> float:
        return (
            self.weights_gb
            + self.gradients_gb
            + self.optimizer_gb
            + self.master_gb
            + self.activations_gb
            + self.overhead_gb
        )

    def dominant_term(self) -> tuple[str, float]:
        parts = {
            "weights": self.weights_gb,
            "gradients": self.gradients_gb,
            "optimizer state": self.optimizer_gb,
            "fp32 master weights": self.master_gb,
            "activations": self.activations_gb,
        }
        return max(parts.items(), key=lambda kv: kv[1])


@dataclass
class CheckReport:
    """Full result of checking one config."""

    config: TrainConfig
    effective_batch: int
    vram: VramBreakdown
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Effective batch and VRAM accounting
# ---------------------------------------------------------------------------


def effective_batch(cfg: TrainConfig) -> int:
    """Sequences whose gradients contribute to one optimizer step.

    Peak memory only ever sees the micro-batch; the optimizer and the
    learning-rate band see this product.
    """
    return cfg.micro_batch * cfg.accumulation_steps * cfg.grad_parallelism


def vram_breakdown(cfg: TrainConfig) -> VramBreakdown:
    """Estimate mixed-precision training state, in GB, before the run.

    Per-device accounting for plain data parallelism: every rank holds the
    full weights, gradients, optimizer state, and master copy. Only the
    activation term depends on micro-batch and sequence length; gradient
    checkpointing collapses it by discarding and recomputing intermediates.
    """
    weight_bytes = WEIGHT_BYTES.get(cfg.weight_dtype, 2.0)
    weights = cfg.base_params_b * weight_bytes

    trainable_b = cfg.base_params_b * cfg.trainable_frac
    gradients = trainable_b * GRAD_BYTES
    optimizer = trainable_b * (MOMENT_BYTES if cfg.optimizer == "adamw" else 0.0)
    master = trainable_b * MASTER_BYTES

    tensors = (
        ACTIVATION_TENSORS["checkpointing"]
        if cfg.gradient_checkpointing
        else ACTIVATION_TENSORS["full"]
    )
    activations = (
        cfg.micro_batch
        * cfg.max_seq_len
        * cfg.hidden_size
        * cfg.num_layers
        * ACTIVATION_BYTES
        * tensors
        / 1e9
    )

    return VramBreakdown(
        weights_gb=weights,
        gradients_gb=gradients,
        optimizer_gb=optimizer,
        master_gb=master,
        activations_gb=activations,
        overhead_gb=OVERHEAD_GB,
    )


# ---------------------------------------------------------------------------
# 3. Learning-rate schedule (linear warmup, cosine or linear decay)
# ---------------------------------------------------------------------------


def lr_at_step(step: int, cfg: TrainConfig) -> float:
    """Learning rate at a 1-based optimizer step.

    Linear warmup from 0 to peak over the first warmup_ratio * total_steps
    steps, then cosine decay (default) or linear decay to ~0 at the last
    step. The schedule counts optimizer steps, not micro-batches.
    """
    if cfg.peak_lr is None or cfg.total_steps <= 0:
        return 0.0
    warmup_steps = int(cfg.total_steps * (cfg.warmup_ratio or 0.0))
    if warmup_steps > 0 and step <= warmup_steps:
        return cfg.peak_lr * step / warmup_steps
    decay_span = max(1, cfg.total_steps - warmup_steps)
    progress = min(1.0, max(0.0, (step - warmup_steps) / decay_span))
    if cfg.lr_schedule == "linear":
        return cfg.peak_lr * (1.0 - progress)
    return cfg.peak_lr * 0.5 * (1.0 + math.cos(math.pi * progress))


def schedule_preview(cfg: TrainConfig, steps: list[int]) -> list[tuple[int, float]]:
    """LR at a few landmark steps, for the printed schedule table."""
    return [(step, lr_at_step(step, cfg)) for step in steps]


# ---------------------------------------------------------------------------
# 4. Finding rules (TRN001-TRN008)
# ---------------------------------------------------------------------------


def check_effective_batch(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN001: reported effective batch does not match micro x accum x devices."""
    computed = effective_batch(cfg)
    if cfg.reported_effective_batch != computed:
        reported = cfg.reported_effective_batch
        claim = "missing" if reported is None else str(reported)
        findings.append(
            Finding(
                severity="critical",
                code="TRN001",
                line="reported_effective_batch",
                message=(
                    f"Config claims effective batch {claim}, but micro_batch "
                    f"{cfg.micro_batch} x accumulation_steps "
                    f"{cfg.accumulation_steps} x grad_parallelism "
                    f"{cfg.grad_parallelism} = {computed}. Accumulation was "
                    "not accounted, so the LR and schedule were planned for "
                    "the wrong batch; record the computed value."
                ),
            )
        )


def check_precision(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN002: bf16 on sm_75 with no fallback — Turing has no native bf16."""
    if (
        cfg.precision == "bf16"
        and cfg.compute_capability == "sm_75"
        and not cfg.allow_precision_fallback
    ):
        findings.append(
            Finding(
                severity="critical",
                code="TRN002",
                line="precision",
                message=(
                    "bf16 is not supported on sm_75 (Turing): native bf16 "
                    "tensor cores start at Ampere sm_80, so the run errors "
                    "or falls back to slow fp32 paths. Use fp16 + autocast + "
                    "GradScaler on this machine, or declare a fallback."
                ),
            )
        )


def check_peak_lr(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN003: peak LR missing or outside the chosen method's sane band."""
    band = LR_BANDS.get(cfg.method)
    if band is None:
        return
    if cfg.peak_lr is None:
        findings.append(
            Finding(
                severity="critical",
                code="TRN003",
                line="peak_lr",
                message=(
                    f"peak_lr is missing; cannot verify it against the "
                    f"{cfg.method} band [{band[0]:.0e}, {band[1]:.0e}]. "
                    "Set an explicit learning rate before launching."
                ),
            )
        )
        return
    low, high = band
    if not low <= cfg.peak_lr <= high:
        findings.append(
            Finding(
                severity="critical",
                code="TRN003",
                line="peak_lr",
                message=(
                    f"peak_lr {cfg.peak_lr:.1e} is outside the {cfg.method} "
                    f"band [{low:.0e}, {high:.0e}]. Full fine-tuning moves "
                    "every weight and needs a small LR; LoRA moves a tiny "
                    "subspace and needs a higher one. A pretraining-scale "
                    "learning rate destroys the weights."
                ),
            )
        )


def check_warmup(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN004: warmup ratio missing or zero — the first steps get full LR."""
    if cfg.warmup_ratio is None or cfg.warmup_ratio <= 0:
        findings.append(
            Finding(
                severity="warning",
                code="TRN004",
                line="warmup_ratio",
                message=(
                    "warmup_ratio is missing or zero. Adam's moments are "
                    "uncalibrated at step 1, so a full-LR first update can "
                    "spike the loss permanently; warm up linearly over 3-5% "
                    "of total steps, expressed as a ratio."
                ),
            )
        )


def check_prompt_masking(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN005: SFT without prompt masking trains on the user's question."""
    if not cfg.prompt_masking:
        findings.append(
            Finding(
                severity="critical",
                code="TRN005",
                line="prompt_masking",
                message=(
                    "prompt_masking is off: loss would be computed on prompt "
                    "tokens too, spending capacity learning to predict the "
                    "user's question. Set prompt positions to -100 so only "
                    "answer tokens contribute gradients."
                ),
            )
        )


def check_vram(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN006: estimated training state exceeds the VRAM budget."""
    vram = vram_breakdown(cfg)
    if vram.total_gb > cfg.vram_budget_gb:
        term, value = vram.dominant_term()
        findings.append(
            Finding(
                severity="critical",
                code="TRN006",
                line="vram_budget_gb",
                message=(
                    f"Estimated training state is {vram.total_gb:.1f} GB, "
                    f"over the {cfg.vram_budget_gb:.1f} GB budget; {term} "
                    f"dominates at {value:.1f} GB. Budget weights + "
                    "gradients + optimizer + activations + overhead before "
                    "launch; an OOM at step 40 is wrong arithmetic, not "
                    "bad luck."
                ),
            )
        )


def check_eval_split(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN007: no eval set distinct from train — leaked metrics, fiction."""
    if cfg.eval_path is None or cfg.eval_path == cfg.train_path:
        shown = cfg.eval_path if cfg.eval_path is not None else "missing"
        findings.append(
            Finding(
                severity="critical",
                code="TRN007",
                line="eval_path",
                message=(
                    f"eval_path is {shown}, not a split distinct from "
                    "train_path. A leaked eval set measures memorization, "
                    "not capability: split train/validation/test from the "
                    "raw data before training and deduplicate across the "
                    "splits."
                ),
            )
        )


def check_checkpoint_metric(cfg: TrainConfig, findings: list[Finding]) -> None:
    """TRN008: checkpoint selection on train loss ships the most overfit save."""
    metric = cfg.checkpoint_metric
    if metric is None or "train" in metric.lower():
        shown = metric if metric is not None else "missing"
        findings.append(
            Finding(
                severity="critical",
                code="TRN008",
                line="checkpoint_metric",
                message=(
                    f"checkpoint_metric is '{shown}', not a held-out "
                    "metric. Selection on train loss ships the most "
                    "overfit checkpoint; select on eval loss during "
                    "training or a task metric at the end, and keep the "
                    "best plus the last."
                ),
            )
        )


def validate(cfg: TrainConfig) -> list[Finding]:
    """Run every TRN00x rule over one config, in code order."""
    findings: list[Finding] = []
    check_effective_batch(cfg, findings)
    check_precision(cfg, findings)
    check_peak_lr(cfg, findings)
    check_warmup(cfg, findings)
    check_prompt_masking(cfg, findings)
    check_vram(cfg, findings)
    check_eval_split(cfg, findings)
    check_checkpoint_metric(cfg, findings)
    return findings


def check_config(cfg: TrainConfig) -> CheckReport:
    """Validate one config and package the numbers the report prints."""
    return CheckReport(
        config=cfg,
        effective_batch=effective_batch(cfg),
        vram=vram_breakdown(cfg),
        findings=validate(cfg),
    )


# ---------------------------------------------------------------------------
# 5. Reporting
# ---------------------------------------------------------------------------


def render_report(report: CheckReport) -> str:
    """Render one config check as a human-readable report."""
    cfg = report.config
    vram = report.vram
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"Training config check: {cfg.name}")
    lines.append("=" * 72)
    lines.append(
        f"Method: {cfg.method}  base: {cfg.base_params_b:g}B  "
        f"weights: {cfg.weight_dtype}  trainable: {cfg.trainable_frac:g}"
    )
    lines.append(
        f"Precision: {cfg.precision} on {cfg.compute_capability}  "
        f"optimizer: {cfg.optimizer}  scaler: "
        f"{'on' if cfg.loss_scaler else 'off'}"
    )
    lines.append(
        f"Effective batch: {cfg.micro_batch} micro x "
        f"{cfg.accumulation_steps} accum x {cfg.grad_parallelism} devices "
        f"= {report.effective_batch}"
    )
    lines.append(
        f"VRAM estimate: {vram.total_gb:.2f} GB of "
        f"{cfg.vram_budget_gb:.1f} GB "
        f"(weights {vram.weights_gb:.2f} + gradients {vram.gradients_gb:.2f} "
        f"+ optimizer {vram.optimizer_gb:.2f} + master {vram.master_gb:.2f} "
        f"+ activations {vram.activations_gb:.2f} "
        f"+ overhead {vram.overhead_gb:.2f})"
    )
    lines.append(
        f"Findings: {len(report.findings)} "
        f"({report.critical_count} critical, {report.warning_count} warning)"
    )
    lines.append("")
    if not report.findings:
        lines.append(
            "No findings. Effective batch, precision, LR band, warmup, "
            "prompt masking, memory, split, and checkpoint metric all "
            "check out."
        )
        return "\n".join(lines)
    order = {"critical": 0, "warning": 1}
    for finding in sorted(report.findings, key=lambda f: order[f.severity]):
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {finding.line}")
        lines.append(f"             {finding.message}")
        lines.append("")
    return "\n".join(lines)


def render_lr_schedule(cfg: TrainConfig) -> str:
    """Render the LR at landmark steps for one config."""
    peak = cfg.peak_lr if cfg.peak_lr is not None else 0.0
    warmup_steps = int(cfg.total_steps * (cfg.warmup_ratio or 0.0))
    probes = sorted(
        {1, warmup_steps, cfg.total_steps // 4, cfg.total_steps // 2, cfg.total_steps}
    )
    lines: list[str] = []
    lines.append("-" * 72)
    lines.append(
        f"LR schedule: {cfg.lr_schedule} decay, peak {peak:.1e}, "
        f"warmup {cfg.warmup_ratio if cfg.warmup_ratio is not None else 0:.0%} "
        f"of {cfg.total_steps} steps ({warmup_steps} warmup steps)"
    )
    lines.append("-" * 72)
    for step, lr in schedule_preview(cfg, probes):
        note = ""
        if warmup_steps > 0 and step <= warmup_steps:
            note = "  (warmup)"
        if step == warmup_steps and warmup_steps > 0:
            note = "  (peak reached)"
        if step == cfg.total_steps:
            note = "  (end)"
        lines.append(f"  step {step:5d} -> {lr:.2e}{note}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 6. Sample packs: a misconfigured run and a sound one
# ---------------------------------------------------------------------------

# BAD pack: 7B full fine-tune on a 16 GB Turing card. Over budget, bf16
# without a fallback, no warmup, LR in the pretraining range, accumulation
# not accounted, no prompt masking, eval leaked from train, checkpoints
# selected on train loss. Raises all eight TRN00x findings.
BAD_CONFIG = TrainConfig(
    name="bad-full-ft-7b",
    method="full",
    base_params_b=7.0,
    weight_dtype="fp16",
    trainable_frac=1.0,
    optimizer="adamw",
    precision="bf16",  # TRN002: no native bf16 on sm_75
    compute_capability="sm_75",
    allow_precision_fallback=False,
    loss_scaler=False,
    micro_batch=4,
    accumulation_steps=8,
    grad_parallelism=1,
    reported_effective_batch=4,  # TRN001: accumulation ignored
    max_seq_len=4096,
    gradient_checkpointing=False,
    peak_lr=5e-4,  # TRN003: pretraining-scale LR on a full fine-tune
    warmup_ratio=0.0,  # TRN004: no warmup
    lr_schedule="cosine",
    total_steps=1000,
    prompt_masking=False,  # TRN005: loss on the user's question
    train_path="data/sft-train.jsonl",
    eval_path="data/sft-train.jsonl",  # TRN007: eval is train
    checkpoint_metric="train_loss",  # TRN008: most overfit checkpoint wins
    vram_budget_gb=16.0,  # estimate ~139 GB -> TRN006
)

# GOOD pack: 7B QLoRA on the same card. 4-bit frozen base, adapters only,
# fp16 with a loss scaler, effective batch recorded correctly, 5% warmup,
# LR inside the LoRA band, prompt masking on, held-out eval split, and
# checkpoint selection on eval loss. Raises zero findings.
GOOD_CONFIG = TrainConfig(
    name="good-qlora-7b",
    method="qlora",
    base_params_b=7.0,
    weight_dtype="int4",
    trainable_frac=0.005,
    optimizer="adamw",
    precision="fp16",
    compute_capability="sm_75",
    allow_precision_fallback=False,
    loss_scaler=True,
    micro_batch=2,
    accumulation_steps=8,
    grad_parallelism=1,
    reported_effective_batch=16,  # 2 x 8 x 1, computed and recorded
    max_seq_len=2048,
    gradient_checkpointing=True,
    peak_lr=2e-4,  # inside the LoRA/QLoRA band [5e-5, 1e-3]
    warmup_ratio=0.05,
    lr_schedule="cosine",
    total_steps=1000,
    prompt_masking=True,
    train_path="data/sft-train.jsonl",
    eval_path="data/sft-eval.jsonl",
    checkpoint_metric="eval_loss",
    vram_budget_gb=16.0,
)

EXPECTED_CODES = {
    "TRN001",
    "TRN002",
    "TRN003",
    "TRN004",
    "TRN005",
    "TRN006",
    "TRN007",
    "TRN008",
}


# ---------------------------------------------------------------------------
# 7. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    """Check a given JSON config, or run the built-in bad/good demo."""
    if len(argv) > 1:
        path = Path(argv[1])
        if not path.is_file():
            print(f"Not a file: {path}", file=sys.stderr)
            return 2
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Cannot read a JSON config from {path}: {exc}", file=sys.stderr)
            return 2
        if not isinstance(data, dict):
            print(f"Expected a JSON object of config fields in {path}", file=sys.stderr)
            return 2
        report = check_config(TrainConfig.from_dict(data))
        print(render_report(report))
        return 1 if report.critical_count else 0

    print("Fine-Tuning 07: LLM Training Internals")
    print("Training-config validator + VRAM planner (stdlib only).")
    print("Running the built-in demo against a bad pack and a good pack.")
    print("Pass a JSON file to validate a real config, for example:")
    print("    python 07-training-internals.py path/to/train-config.json")
    print()

    bad_report = check_config(BAD_CONFIG)
    print(render_report(bad_report))
    print()

    good_report = check_config(GOOD_CONFIG)
    print(render_report(good_report))
    print()

    print(render_lr_schedule(GOOD_CONFIG))
    print()

    # Demo invariants: the arithmetic and the rules themselves.
    bad_codes = {f.code for f in bad_report.findings}
    assert bad_codes == EXPECTED_CODES, (
        f"bad pack must raise all eight codes, got {bad_codes}"
    )
    assert good_report.findings == [], "good pack must raise zero findings"
    assert effective_batch(BAD_CONFIG) == 32, "4 micro x 8 accum x 1 device = 32"
    assert effective_batch(GOOD_CONFIG) == 16, "2 micro x 8 accum x 1 device = 16"
    bad_vram = vram_breakdown(BAD_CONFIG)
    good_vram = vram_breakdown(GOOD_CONFIG)
    assert bad_vram.total_gb > 100.0, "7B full FT exceeds 100 GB of training state"
    assert bad_vram.dominant_term()[0] == "optimizer state", "AdamW moments dominate"
    assert 3.0 < good_vram.total_gb < 16.0, "7B QLoRA fits a 16 GB card"
    peak = GOOD_CONFIG.peak_lr
    assert peak is not None
    assert lr_at_step(1, GOOD_CONFIG) < peak, "warmup starts below peak"
    assert abs(lr_at_step(50, GOOD_CONFIG) - peak) < 1e-12, "peak reached at warmup end"
    assert lr_at_step(500, GOOD_CONFIG) < lr_at_step(250, GOOD_CONFIG), "cosine decays"
    assert lr_at_step(1000, GOOD_CONFIG) == 0.0, "decay lands on ~0 at the last step"

    print("-" * 72)
    print(
        f"Demo result: bad pack raised {len(bad_report.findings)} findings "
        f"({', '.join(sorted(bad_codes))}); good pack raised "
        f"{len(good_report.findings)} findings (zero)."
    )
    print("all asserts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
