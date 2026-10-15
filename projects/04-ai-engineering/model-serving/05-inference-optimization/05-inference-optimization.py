"""
Exercise 05: Inference Optimization Policy Checker
===================================================
Check a serving configuration against the seven sizing and safety rules from
Lecture 05 (Model Serving 05: Inference Optimization) before the config ever
reaches a GPU: budget fit, precision consistency, bounded context, the
quantization eval gate, a latency objective under batching, a terminal
fallback hop, and speculative decoding at large batch.

This exercise is deliberately runnable without a GPU or an engine installed.
It does the arithmetic the lecture does by hand: weights, KV cache from
layers x 2 x kv_heads x head_dim x dtype_bytes x seq_len x batch, and runtime
overhead, against a declared budget.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python 05-inference-optimization.py
    python 05-inference-optimization.py path/to/serving-config.json
    python 05-inference-optimization.py --dump-sample good > config.json

Exit codes:
    0  no critical findings (demo mode also runs its self-test)
    1  at least one critical finding (path mode)
    2  usage error, unreadable file, or invalid JSON
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------

FALLBACK_CONTEXT = 8192  # an unbounded config still reserves a full context
SPECULATIVE_BATCH_LIMIT = 4

# Storage bytes per parameter for precisions with an exact width. Quant
# formats (q4_k_m, awq, gptq, ...) are exempt: their real width depends on
# scales and block overhead, so only a declared exact precision can contradict
# bytes_per_param.
EXACT_PRECISION_BYTES = {
    "fp32": 4.0,
    "fp16": 2.0,
    "bf16": 2.0,
    "fp8": 1.0,
    "int8": 1.0,
    "int4": 0.5,
    "uint4": 0.5,
}
FULL_PRECISION = {"fp32", "fp16", "bf16"}

# A fallback ladder must end somewhere honest. Substrings are matched against
# lowercased hop names, so "degraded-response" counts. Bare words like "fail"
# are deliberately absent: they match ordinary model names.
TERMINAL_HOP_MARKERS = (
    "degraded",
    "offline",
    "unavailable",
    "abstain",
    "graceful",
    "error",
    "503",
)

ALL_CODES = (
    "INF001",
    "INF002",
    "INF003",
    "INF004",
    "INF005",
    "INF006",
    "INF007",
)


@dataclass
class HardwareSpec:
    """The card the configuration must fit on."""

    device_name: str
    vram_gb: float


@dataclass
class ModelSpec:
    """Model shape and storage precision, enough to size weights and KV."""

    name: str
    params_b: float
    precision: str
    bytes_per_param: float
    layers: int
    kv_heads: int
    head_dim: int
    kv_dtype_bytes: float


@dataclass
class ServingSpec:
    """Engine-side knobs the rules read."""

    engine: str
    max_model_len: int
    batch_size: int
    prefix_caching: bool
    speculative: bool
    latency_slo_ms: int | None


@dataclass
class QualitySpec:
    """The third objective: a floor and the gate that enforces it."""

    quality_floor: float | None
    eval_gate: bool


@dataclass
class RoutingSpec:
    """Ordered fallback ladder for a failing primary."""

    fallback_chain: list[str]


@dataclass
class BudgetPlan:
    """Usable gigabytes and the runtime overhead reserved inside them."""

    budget_gb: float
    runtime_overhead_gb: float


@dataclass
class ServingConfig:
    """One complete serving configuration under review."""

    hardware: HardwareSpec
    model: ModelSpec
    serving: ServingSpec
    quality: QualitySpec
    routing: RoutingSpec
    budget: BudgetPlan


@dataclass
class Finding:
    """A single rule violation against a serving configuration."""

    severity: str  # "critical" | "warning"
    code: str
    line_number: int | None
    message: str


@dataclass
class Analysis:
    """Full analysis result for one configuration."""

    label: str
    config: ServingConfig
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Loading and sizing
# ---------------------------------------------------------------------------


def _section(data: dict, name: str) -> dict:
    """One nested object of the config, or an empty dict when absent."""
    value = data.get(name)
    return value if isinstance(value, dict) else {}


def _opt_int(section: dict, key: str) -> int | None:
    """Optional integer field: absent or null becomes None, never a default."""
    value = section.get(key)
    return None if value is None else int(value)


def _opt_float(section: dict, key: str) -> float | None:
    """Optional float field: absent or null becomes None, never a default."""
    value = section.get(key)
    return None if value is None else float(value)


def config_from_dict(data: dict) -> ServingConfig:
    """Build a ServingConfig from decoded JSON. Missing keys get safe defaults."""
    hw = _section(data, "hardware")
    mo = _section(data, "model")
    se = _section(data, "serving")
    qu = _section(data, "quality")
    ro = _section(data, "routing")
    bu = _section(data, "budget")

    return ServingConfig(
        hardware=HardwareSpec(
            device_name=str(hw.get("device_name", "unknown")),
            vram_gb=float(hw.get("vram_gb", 0.0)),
        ),
        model=ModelSpec(
            name=str(mo.get("name", "unnamed")),
            params_b=float(mo.get("params_b", 0.0)),
            precision=str(mo.get("precision", "fp16")),
            bytes_per_param=float(mo.get("bytes_per_param", 2.0)),
            layers=int(mo.get("layers", 0)),
            kv_heads=int(mo.get("kv_heads", 0)),
            head_dim=int(mo.get("head_dim", 0)),
            kv_dtype_bytes=float(mo.get("kv_dtype_bytes", 2.0)),
        ),
        serving=ServingSpec(
            engine=str(se.get("engine", "unknown")),
            max_model_len=int(se.get("max_model_len", 0)),
            batch_size=int(se.get("batch_size", 1)),
            prefix_caching=bool(se.get("prefix_caching", False)),
            speculative=bool(se.get("speculative", False)),
            latency_slo_ms=_opt_int(se, "latency_slo_ms"),
        ),
        quality=QualitySpec(
            quality_floor=_opt_float(qu, "quality_floor"),
            eval_gate=bool(qu.get("eval_gate", False)),
        ),
        routing=RoutingSpec(
            fallback_chain=[str(hop) for hop in ro.get("fallback_chain", [])],
        ),
        budget=BudgetPlan(
            budget_gb=float(bu.get("budget_gb", 0.0)),
            runtime_overhead_gb=float(bu.get("runtime_overhead_gb", 0.0)),
        ),
    )


def line_of(text: str | None, key: str) -> int | None:
    """First 1-based line carrying "key", so findings point into the JSON file."""
    if text is None:
        return None
    needle = f'"{key}"'
    for number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return number
    return None


def kv_bytes_per_token(model: ModelSpec) -> float:
    """KV cache one sequence pays per token: layers x 2 x kv_heads x head_dim x dtype."""
    return model.layers * 2 * model.kv_heads * model.head_dim * model.kv_dtype_bytes


def weights_gb(config: ServingConfig) -> float:
    """Resident weight storage in decimal GB."""
    return config.model.params_b * config.model.bytes_per_param


def effective_context(config: ServingConfig) -> int:
    """The context the KV reservation is sized at; unbounded falls back to 8192."""
    length = config.serving.max_model_len
    return length if length > 0 else FALLBACK_CONTEXT


def kv_gb(config: ServingConfig) -> float:
    """KV cache in decimal GB at max_model_len and the intended batch size."""
    per_token = kv_bytes_per_token(config.model)
    total_bytes = per_token * effective_context(config) * config.serving.batch_size
    return total_bytes / 1e9


def total_gb(config: ServingConfig) -> float:
    """Weights plus KV plus runtime overhead: the number the budget is compared to."""
    return weights_gb(config) + kv_gb(config) + config.budget.runtime_overhead_gb


# ---------------------------------------------------------------------------
# 3. Rules
# ---------------------------------------------------------------------------


def check_budget_overrun(config: ServingConfig, text: str | None) -> Finding | None:
    """Weights plus KV plus overhead must fit the declared budget (INF001)."""
    total = total_gb(config)
    if total <= config.budget.budget_gb:
        return None
    return Finding(
        severity="critical",
        code="INF001",
        line_number=line_of(text, "budget_gb"),
        message=(
            f"Projected {total:.2f} GB (weights {weights_gb(config):.2f} + "
            f"KV {kv_gb(config):.2f} + overhead "
            f"{config.budget.runtime_overhead_gb:.2f}) exceeds the "
            f"{config.budget.budget_gb:.2f} GB budget."
        ),
    )


def check_precision_mismatch(config: ServingConfig, text: str | None) -> Finding | None:
    """An exact precision must agree with the declared bytes per param (INF002)."""
    precision = config.model.precision.lower()
    expected = EXACT_PRECISION_BYTES.get(precision)
    actual = config.model.bytes_per_param
    if expected is None or abs(actual - expected) <= 1e-6:
        return None
    return Finding(
        severity="critical",
        code="INF002",
        line_number=line_of(text, "precision"),
        message=(
            f"precision '{precision}' stores {expected} bytes/param but "
            f"bytes_per_param is {actual}. Pick one source of truth for the math."
        ),
    )


def check_unbounded_context(config: ServingConfig, text: str | None) -> Finding | None:
    """Prefix caching needs a bounded context to size against (INF003)."""
    serving = config.serving
    if not serving.prefix_caching or serving.max_model_len > 0:
        return None
    return Finding(
        severity="warning",
        code="INF003",
        line_number=line_of(text, "max_model_len"),
        message=(
            f"prefix_caching is on but max_model_len is {serving.max_model_len}; "
            "the cache has no bound to size its reservation against."
        ),
    )


def check_quantization_gate(config: ServingConfig, text: str | None) -> Finding | None:
    """Narrow weights with a quality floor must declare a gate (INF004)."""
    model = config.model
    quality = config.quality
    quantized = model.precision.lower() not in FULL_PRECISION
    if not quantized or quality.quality_floor is None or quality.eval_gate:
        return None
    return Finding(
        severity="warning",
        code="INF004",
        line_number=line_of(text, "eval_gate"),
        message=(
            f"Quantized precision '{model.precision}' with quality_floor "
            f"{quality.quality_floor} but no eval_gate: quantization drift "
            "would ship unverified."
        ),
    )


def check_batch_without_slo(config: ServingConfig, text: str | None) -> Finding | None:
    """Batching above one without a latency objective hides the crossing (INF005)."""
    serving = config.serving
    if serving.batch_size <= 1 or serving.latency_slo_ms is not None:
        return None
    return Finding(
        severity="warning",
        code="INF005",
        line_number=line_of(text, "latency_slo_ms"),
        message=(
            f"batch_size {serving.batch_size} with no latency_slo_ms: batching "
            "to saturation hides the point where p95 crosses the objective."
        ),
    )


def check_fallback_terminal(config: ServingConfig, text: str | None) -> Finding | None:
    """The ladder must end in an honest degraded hop (INF006)."""
    chain = config.routing.fallback_chain
    has_terminal = any(
        any(marker in hop.lower() for marker in TERMINAL_HOP_MARKERS) for hop in chain
    )
    if has_terminal:
        return None
    return Finding(
        severity="critical",
        code="INF006",
        line_number=line_of(text, "fallback_chain"),
        message=(
            f"fallback_chain {chain} has no terminal degraded hop; a failing "
            "primary has nowhere to land and the request hangs."
        ),
    )


def check_speculative_batch(config: ServingConfig, text: str | None) -> Finding | None:
    """Speculative drafting rarely pays at large batch (INF007)."""
    serving = config.serving
    if not serving.speculative or serving.batch_size <= SPECULATIVE_BATCH_LIMIT:
        return None
    return Finding(
        severity="warning",
        code="INF007",
        line_number=line_of(text, "speculative"),
        message=(
            f"speculative decoding at batch_size {serving.batch_size} "
            f"(limit {SPECULATIVE_BATCH_LIMIT}): drafting rarely pays above "
            "small batches. Measure acceptance rate and tokens/sec first."
        ),
    )


CHECKS = (
    check_budget_overrun,
    check_precision_mismatch,
    check_unbounded_context,
    check_quantization_gate,
    check_batch_without_slo,
    check_fallback_terminal,
    check_speculative_batch,
)


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze(label: str, config: ServingConfig, text: str | None = None) -> Analysis:
    """Run every rule against one configuration."""
    analysis = Analysis(label=label, config=config)
    for check in CHECKS:
        finding = check(config, text)
        if finding is not None:
            analysis.findings.append(finding)
    return analysis


def render(analysis: Analysis) -> str:
    """Render a human-readable report."""
    config = analysis.config
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"Serving config review: {analysis.label}")
    lines.append("=" * 72)
    lines.append(
        f"Engine: {config.serving.engine}  "
        f"Model: {config.model.name} ({config.model.params_b}B, "
        f"{config.model.precision})"
    )
    context_note = ""
    if config.serving.max_model_len <= 0:
        context_note = " [unbounded, sized at 8192]"
    lines.append(
        f"Batch: {config.serving.batch_size}  "
        f"Context: {config.serving.max_model_len}{context_note}  "
        f"VRAM: {config.hardware.vram_gb:.2f} GB"
    )
    lines.append(
        f"Budget: weights {weights_gb(config):.2f} + KV {kv_gb(config):.2f} + "
        f"overhead {config.budget.runtime_overhead_gb:.2f} = "
        f"{total_gb(config):.2f} GB of {config.budget.budget_gb:.2f} GB"
    )
    lines.append(
        f"Findings: {analysis.critical_count} critical, "
        f"{analysis.warning_count} warning"
    )
    lines.append("")

    if not analysis.findings:
        lines.append("No findings. This config passes every rule in this exercise.")
        return "\n".join(lines)

    order = {"critical": 0, "warning": 1}
    for finding in sorted(analysis.findings, key=lambda f: order[f.severity]):
        location = f"L{finding.line_number}" if finding.line_number else "--"
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {location}")
        lines.append(f"             {finding.message}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample configurations used for the demo
# ---------------------------------------------------------------------------

# Fits the 16 GB card: 7.6B x 0.6 bytes = 4.56 GB weights, 28 layers x 2 x
# 8 kv heads x 128 x 2 bytes = 114,688 B/token, x 8192 x batch 4 = 3.76 GB KV,
# plus 1.5 GB overhead: 9.82 GB total.
GOOD = {
    "hardware": {"device_name": "NVIDIA Quadro RTX 5000", "vram_gb": 16.0},
    "model": {
        "name": "qwen2.5-coder:7b",
        "params_b": 7.6,
        "precision": "q4_k_m",
        "bytes_per_param": 0.6,
        "layers": 28,
        "kv_heads": 8,
        "head_dim": 128,
        "kv_dtype_bytes": 2.0,
    },
    "serving": {
        "engine": "ollama",
        "max_model_len": 8192,
        "batch_size": 4,
        "prefix_caching": True,
        "speculative": True,
        "latency_slo_ms": 800,
    },
    "quality": {"quality_floor": 0.90, "eval_gate": True},
    "routing": {
        "fallback_chain": [
            "local-qwen2.5-coder-7b",
            "cloud-mid-model",
            "cached-answer",
            "degraded-response",
        ]
    },
    "budget": {"budget_gb": 16.0, "runtime_overhead_gb": 1.5},
}

# Violates every rule: 52 GB of weights against a 16 GB budget, a precision
# that contradicts bytes_per_param, an unbounded context under prefix
# caching, a quality floor with no gate, batching with no SLO, a ladder with
# no terminal hop, and drafting at batch 8.
BAD = {
    "hardware": {"device_name": "NVIDIA Quadro RTX 5000", "vram_gb": 16.0},
    "model": {
        "name": "llama-2-13b-chat",
        "params_b": 13.0,
        "precision": "int4",
        "bytes_per_param": 4.0,
        "layers": 40,
        "kv_heads": 40,
        "head_dim": 128,
        "kv_dtype_bytes": 2.0,
    },
    "serving": {
        "engine": "vllm",
        "max_model_len": 0,
        "batch_size": 8,
        "prefix_caching": True,
        "speculative": True,
        "latency_slo_ms": None,
    },
    "quality": {"quality_floor": 0.85, "eval_gate": False},
    "routing": {"fallback_chain": ["llama-2-13b-local", "cloud-frontier-api"]},
    "budget": {"budget_gb": 16.0, "runtime_overhead_gb": 1.5},
}


def analyze_sample(sample: dict, label: str) -> Analysis:
    """Analyze a built-in sample through the same path a JSON file takes."""
    text = json.dumps(sample, indent=2)
    return analyze(label, config_from_dict(sample), text)


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------


def run_demo() -> int:
    """Print both sample reports, then assert the rules behave as documented."""
    print("Inference Optimization Exercise 05")
    print("Seven rules from Lecture 05, checked against two sample configs.")
    print("Check your own:  python 05-inference-optimization.py config.json")
    print("Export a sample: python 05-inference-optimization.py --dump-sample good")
    print()

    good = analyze_sample(GOOD, "GOOD sample")
    bad = analyze_sample(BAD, "BAD sample")
    print(render(bad))
    print()
    print(render(good))

    # Break the GOOD config on purpose: a declared fp16 width of 4.0
    # bytes/param must trip the precision rule (and the budget with it).
    mirror_model = replace(good.config.model, precision="fp16", bytes_per_param=4.0)
    mirror = analyze(
        "GOOD sample with a broken precision", replace(good.config, model=mirror_model)
    )

    good_codes = {f.code for f in good.findings}
    bad_codes = {f.code for f in bad.findings}
    mirror_codes = {f.code for f in mirror.findings}
    good_total = total_gb(good.config)

    assert good_codes == set(), f"GOOD must be clean, got {sorted(good_codes)}"
    assert bad_codes == set(ALL_CODES), (
        f"BAD must raise all {len(ALL_CODES)} codes, got {sorted(bad_codes)}"
    )
    assert "INF002" in mirror_codes, "Breaking the precision must fire INF002"
    assert 9.8 <= good_total <= 9.9, (
        f"GOOD total should be 9.8 GB, got {good_total:.3f}"
    )

    print("-" * 72)
    print(
        f"Demo result: BAD raised {bad.critical_count} critical and "
        f"{bad.warning_count} warning findings; GOOD raised none."
    )
    print(
        f"Self-test passed: GOOD clean, BAD hit all {len(ALL_CODES)} codes, "
        f"broken precision fired INF002, GOOD total {good_total:.2f} GB."
    )
    return 0


def main(argv: list[str]) -> int:
    """Check a JSON config, dump a sample, or run the built-in demo."""
    if len(argv) > 1 and argv[1] == "--dump-sample":
        which = argv[2].lower() if len(argv) > 2 else "good"
        if which not in {"good", "bad"}:
            print("Usage: --dump-sample [good|bad]", file=sys.stderr)
            return 2
        print(json.dumps(BAD if which == "bad" else GOOD, indent=2))
        return 0

    if len(argv) > 1:
        target = Path(argv[1])
        if not target.is_file():
            print(f"Not a file: {target}", file=sys.stderr)
            return 2
        # utf-8-sig strips a BOM editors on this machine like to add; anything
        # else (a UTF-16 redirect, binary) exits 2 instead of tracebacks.
        try:
            text = target.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            print(f"Cannot read {target} as UTF-8: {exc}", file=sys.stderr)
            return 2
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON in {target}: {exc}", file=sys.stderr)
            return 2
        if not isinstance(data, dict):
            print(f"Expected a JSON object in {target}", file=sys.stderr)
            return 2
        analysis = analyze(str(target), config_from_dict(data), text)
        print(render(analysis))
        return 1 if analysis.critical_count else 0

    return run_demo()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
