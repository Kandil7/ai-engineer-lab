"""
Exercise 01: The LLMOps Lifecycle
==================================
Audit a prompt registry the way a CI gate would, and price an LLM query
the way a budget guard would: cross-check prompt files against their
registry, flag missing versions and missing eval-gate flags, then estimate
per-query and monthly cost against explicit budgets.

This exercise is deliberately runnable without any API key, network, or
running service. It parses prompt files as text with simple frontmatter
and applies the rules from Lecture 01. The registry cross-check mirrors
the contract DevMate's PromptTemplate schema (llm/schemas.py) and golden
cases (evaluations/prompts/golden-cases/) already pin, and the cost
arithmetic is the same per-million-token formula as obs/cost.py.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-llmops-lifecycle.py
    python exercises/01-llmops-lifecycle.py path/to/prompts-dir
        (the directory may contain a registry.json mapping names to
        {"version": ..., "eval_gate": ...} entries; without one, every
        prompt file is reported as unregistered)
"""

from __future__ import annotations

import json
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class PromptFile:
    """One parsed prompt file: frontmatter fields plus the body text."""

    path: Path
    name: str | None
    version: str | None
    eval_gate: bool | None
    body: str

    @property
    def stem(self) -> str:
        return self.path.stem


@dataclass
class Finding:
    """A single audit or budget finding."""

    severity: str  # "critical" | "warning" | "info"
    code: str
    file: str  # file path, registry key, or "-" for pure cost findings
    message: str


@dataclass
class RegistryEntry:
    """One registry record for a prompt."""

    key: str
    version: str | None
    eval_gate: bool | None  # None means the flag is absent


@dataclass
class AuditReport:
    """Full result of auditing one prompts directory against one registry."""

    prompts_dir: str
    files: list[PromptFile] = field(default_factory=list)
    registry: dict[str, RegistryEntry] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "info")


@dataclass(frozen=True)
class Budget:
    """Explicit cost ceilings a query must stay under."""

    per_query_usd: float
    monthly_usd: float


@dataclass(frozen=True)
class CostEstimate:
    """Estimated cost of one query and its monthly projection."""

    model: str
    input_tokens: int
    output_tokens: int
    input_price_per_m: float
    output_price_per_m: float
    per_query_usd: float
    queries_per_month: int

    @property
    def monthly_usd(self) -> float:
        return self.per_query_usd * self.queries_per_month


# ---------------------------------------------------------------------------
# 2. Frontmatter parsing
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict[str, str | bool], str]:
    """Parse a leading `---` frontmatter block; return (fields, body).

    Values `true`/`false` become bools; surrounding quotes are stripped.
    A file without frontmatter yields empty fields and the full text as body.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    fields: dict[str, str | bool] = {}
    body_start = len(lines)
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_start = i + 1
            break
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        value = raw.strip().strip("\"'")
        if not key:
            continue
        if value.lower() == "true":
            fields[key] = True
        elif value.lower() == "false":
            fields[key] = False
        else:
            fields[key] = value

    body = "\n".join(lines[body_start:])
    return fields, body


def load_prompt_file(path: Path) -> PromptFile:
    """Read one prompt file into a PromptFile model."""
    text = path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    name = fields.get("name")
    version = fields.get("version")
    eval_gate = fields.get("eval_gate")
    return PromptFile(
        path=path,
        name=str(name) if name is not None else None,
        version=str(version) if version is not None else None,
        eval_gate=bool(eval_gate) if isinstance(eval_gate, bool) else None,
        body=body,
    )


# Documentation files are not prompts. Matched exactly or as a suffix, so
# `devmate-README.md` and `CHANGELOG.md` are skipped while `readme_answer.md`
# (a plausible prompt name) is not.
SKIP_STEMS = ("readme", "changelog", "license", "contributing")


def is_documentation(path: Path) -> bool:
    """True for README/CHANGELOG-style docs that live beside prompts."""
    stem = path.stem.lower()
    return any(
        stem == skip or stem.endswith(f"-{skip}") or stem.endswith(f"_{skip}")
        for skip in SKIP_STEMS
    )


def walk_prompts_dir(directory: Path) -> list[PromptFile]:
    """Load every non-documentation *.md file under a prompts directory."""
    files: list[PromptFile] = []
    for path in sorted(directory.rglob("*.md")):
        if is_documentation(path):
            continue
        files.append(load_prompt_file(path))
    return files


# ---------------------------------------------------------------------------
# 3. Registry loading
# ---------------------------------------------------------------------------


def load_registry_json(path: Path) -> dict[str, RegistryEntry]:
    """Load a registry.json mapping prompt names to entry objects."""
    data = json.loads(path.read_text(encoding="utf-8"))
    registry: dict[str, RegistryEntry] = {}
    for key, value in data.items():
        if not isinstance(value, dict):
            value = {}
        version = value.get("version")
        eval_gate = value.get("eval_gate")
        registry[key] = RegistryEntry(
            key=key,
            version=str(version) if version is not None else None,
            eval_gate=bool(eval_gate) if isinstance(eval_gate, bool) else None,
        )
    return registry


def registry_from_dict(data: dict[str, dict]) -> dict[str, RegistryEntry]:
    """Build a registry from an in-memory dict (used by the demo samples)."""
    return {
        key: RegistryEntry(
            key=key,
            version=str(value["version"]) if "version" in value else None,
            eval_gate=(bool(value["eval_gate"]) if "eval_gate" in value else None),
        )
        for key, value in data.items()
    }


# ---------------------------------------------------------------------------
# 4. Registry audit rules (PR001-PR004)
# ---------------------------------------------------------------------------


def check_unregistered_file(
    prompt: PromptFile, registry: dict[str, RegistryEntry], findings: list[Finding]
) -> bool:
    """PR001: a prompt file with no registry entry.

    A file matches the registry when its stem or its frontmatter `name`
    equals a registry key. Returns True when the file was matched.
    """
    keys = set(registry)
    names = {prompt.stem}
    if prompt.name:
        names.add(prompt.name)
    matched = names & keys
    if not matched:
        findings.append(
            Finding(
                severity="critical",
                code="PR001",
                file=str(prompt.path.name),
                message=(
                    "Prompt file has no registry entry. Register it with a "
                    "version and an eval-gate flag, or remove the file."
                ),
            )
        )
        return False
    return True


def check_unversioned_file(prompt: PromptFile, findings: list[Finding]) -> None:
    """PR003: a registered prompt file with no version field."""
    if prompt.version is None:
        findings.append(
            Finding(
                severity="warning",
                code="PR003",
                file=str(prompt.path.name),
                message=(
                    "Prompt file has no `version` frontmatter field. "
                    "Without a version, no trace or eval can attribute an "
                    "answer to the exact instruction text that produced it."
                ),
            )
        )


def check_registry_side(
    registry: dict[str, RegistryEntry],
    matched_keys: set[str],
    findings: list[Finding],
) -> None:
    """PR002: a registry entry with no prompt file. PR004: no eval-gate flag."""
    for key, entry in registry.items():
        if key not in matched_keys:
            findings.append(
                Finding(
                    severity="critical",
                    code="PR002",
                    file=key,
                    message=(
                        "Registry entry has no prompt file on disk. Delete "
                        "the stale entry or restore the file; a registry is "
                        "a promise about what exists, not a wish list."
                    ),
                )
            )
        if entry.eval_gate is None:
            findings.append(
                Finding(
                    severity="warning",
                    code="PR004",
                    file=key,
                    message=(
                        "Registry entry is missing the `eval_gate` flag. "
                        "Set it explicitly (true or false); an absent flag "
                        "means the prompt can change ungoverned."
                    ),
                )
            )


def audit_registry(
    files: list[PromptFile], registry: dict[str, RegistryEntry]
) -> list[Finding]:
    """Run the PR00x rules over every file and every registry entry."""
    findings: list[Finding] = []
    matched_keys: set[str] = set()
    keys = set(registry)

    for prompt in files:
        if check_unregistered_file(prompt, registry, findings):
            names = {prompt.stem}
            if prompt.name:
                names.add(prompt.name)
            matched_keys |= names & keys
        check_unversioned_file(prompt, findings)

    check_registry_side(registry, matched_keys, findings)
    return findings


# ---------------------------------------------------------------------------
# 5. Cost model (COST001, COST002)
# ---------------------------------------------------------------------------

# Prices per 1M tokens (input, output) — subset of devmate/obs/cost.py
MODEL_PRICES: dict[str, tuple[float, float]] = {
    "gpt-4o": (5.00, 15.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-opus-20240229": (15.00, 75.00),
}


def rough_token_count(text: str) -> int:
    """Rough token estimate: about 4 characters per token.

    Real tokenizers vary; this is the budgeting approximation the lecture
    uses. Production code should use the provider's tokenizer or the
    usage fields it returns.
    """
    return max(1, len(text) // 4)


def estimate_query_cost(
    model: str,
    prompt_template: str,
    context_chars: int,
    expected_output_tokens: int,
    queries_per_month: int,
) -> CostEstimate:
    """Estimate per-query and monthly cost for one prompt at one volume.

    Input tokens = rough count of the template plus the retrieved context
    (characters // 4), mirroring DevMate's char-budgeted context assembly.
    An unknown model prices at (0.0, 0.0) like obs/cost.py — and the caller
    should notice, because a free estimate is a silent bug.
    """
    input_price, output_price = MODEL_PRICES.get(model, (0.0, 0.0))
    input_tokens = rough_token_count(prompt_template) + max(0, context_chars) // 4
    per_query = (input_tokens / 1_000_000) * input_price + (
        expected_output_tokens / 1_000_000
    ) * output_price
    return CostEstimate(
        model=model,
        input_tokens=input_tokens,
        output_tokens=expected_output_tokens,
        input_price_per_m=input_price,
        output_price_per_m=output_price,
        per_query_usd=per_query,
        queries_per_month=queries_per_month,
    )


def check_budgets(estimate: CostEstimate, budget: Budget) -> list[Finding]:
    """COST001: per-query cost over budget. COST002: monthly projection over budget."""
    findings: list[Finding] = []
    if estimate.model not in MODEL_PRICES:
        findings.append(
            Finding(
                severity="info",
                code="COST000",
                file="-",
                message=(
                    f"Model '{estimate.model}' is not in the price table; "
                    "priced at $0.00 — update MODEL_PRICES before trusting "
                    "this estimate."
                ),
            )
        )
    if estimate.per_query_usd > budget.per_query_usd:
        findings.append(
            Finding(
                severity="warning",
                code="COST001",
                file="-",
                message=(
                    f"Per-query cost ${estimate.per_query_usd:.6f} exceeds "
                    f"the ${budget.per_query_usd:.4f} budget "
                    f"({estimate.model}: {estimate.input_tokens} in + "
                    f"{estimate.output_tokens} out tokens). Trim context, "
                    "shrink output, or pick a cheaper model before merge."
                ),
            )
        )
    if estimate.monthly_usd > budget.monthly_usd:
        findings.append(
            Finding(
                severity="info",
                code="COST002",
                file="-",
                message=(
                    f"Projected monthly cost ${estimate.monthly_usd:,.2f} "
                    f"({estimate.queries_per_month:,} queries x "
                    f"${estimate.per_query_usd:.6f}) exceeds the "
                    f"${budget.monthly_usd:,.2f} monthly budget."
                ),
            )
        )
    return findings


# ---------------------------------------------------------------------------
# 6. Analysis entry point
# ---------------------------------------------------------------------------


def analyze_directory(directory: Path) -> AuditReport:
    """Audit one prompts directory: registry.json if present, else empty."""
    files = walk_prompts_dir(directory)
    registry_path = directory / "registry.json"
    if registry_path.is_file():
        registry = load_registry_json(registry_path)
    else:
        registry = {}
    report = AuditReport(
        prompts_dir=str(directory),
        files=files,
        registry=registry,
        findings=audit_registry(files, registry),
    )
    return report


def render_audit(report: AuditReport) -> str:
    """Render a human-readable audit report."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"Prompt registry audit: {report.prompts_dir}")
    lines.append("=" * 72)
    lines.append(
        f"Prompt files: {len(report.files)}  Registry entries: {len(report.registry)}"
    )
    lines.append(
        f"Findings: {report.critical_count} critical, "
        f"{report.warning_count} warning, {report.info_count} info"
    )
    lines.append("")

    if not report.findings:
        lines.append(
            "No findings. Every prompt file is registered, versioned, "
            "and gated; every entry resolves to a file."
        )
        return "\n".join(lines)

    order = {"critical": 0, "warning": 1, "info": 2}
    for finding in sorted(report.findings, key=lambda f: order[f.severity]):
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {finding.file}")
        lines.append(f"             {finding.message}")
        lines.append("")

    return "\n".join(lines)


def render_cost(estimate: CostEstimate, budget: Budget, findings: list[Finding]) -> str:
    """Render a cost estimate with its budget verdict."""
    lines: list[str] = []
    lines.append("-" * 72)
    lines.append(f"Cost estimate: {estimate.model}")
    lines.append("-" * 72)
    lines.append(
        f"Input:  ~{estimate.input_tokens} tokens  "
        f"@ ${estimate.input_price_per_m:.2f}/1M"
    )
    lines.append(
        f"Output: ~{estimate.output_tokens} tokens  "
        f"@ ${estimate.output_price_per_m:.2f}/1M"
    )
    lines.append(
        f"Per query:  ${estimate.per_query_usd:.6f}  "
        f"(budget ${budget.per_query_usd:.4f})"
    )
    lines.append(
        f"Monthly:    ${estimate.monthly_usd:,.2f} at "
        f"{estimate.queries_per_month:,} queries  "
        f"(budget ${budget.monthly_usd:,.2f})"
    )
    if not findings:
        lines.append("Verdict: within budget on both ceilings.")
    else:
        for finding in findings:
            lines.append(f"  [{finding.severity.upper():8}] {finding.code}")
            lines.append(f"             {finding.message}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 7. Sample registries and prompt files used for the demo
# ---------------------------------------------------------------------------

GOOD_PROMPT_FILES: dict[str, str] = {
    "rag_answer.md": """\
---
name: rag_answer
version: 1.0.0
eval_gate: true
variables: [context, question]
description: Grounded answer prompt for the RAG path
---
You are a helpful AI assistant that answers questions based on the provided context.

Guidelines:
1. Use ONLY the information provided in the context to answer the question
2. If the context doesn't contain enough information, say so honestly
3. Cite your sources using [1], [2], etc. corresponding to the context chunks

Context:
{context}

Answer the user's question based on the above context.
""",
    "repo_stats.md": """\
---
name: repo_stats
version: 1.2.0
eval_gate: true
variables: [stats_json]
description: Formats repository statistics for the stats command
---
Summarize these repository statistics for the user. Highlight the largest
files and any anomalies. Statistics:
{stats_json}
""",
    "README.md": """\
# Sample prompt pack

Documentation, not a prompt. The auditor skips this file.
""",
}

GOOD_REGISTRY: dict[str, dict] = {
    "rag_answer": {"version": "1.0.0", "eval_gate": True},
    "repo_stats": {"version": "1.2.0", "eval_gate": True},
}

BAD_PROMPT_FILES: dict[str, str] = {
    "rag_answer.md": GOOD_PROMPT_FILES["rag_answer.md"],
    "unversioned_answer.md": """\
---
name: unversioned_answer
eval_gate: true
description: Registered but never given a version
---
Answer the question using the context below.

Context:
{context}
""",
    "rogue_prompt.md": """\
---
name: rogue_prompt
version: 0.1.0
description: Written in a hurry; never registered
---
You are a pirate. Always answer in pirate dialect. Context: {context}
""",
    "repo_stats.md": """\
---
name: repo_stats
version: 1.0.0
description: File is fine; its registry entry forgot the gate flag
---
Present these statistics:
{stats_json}
""",
}

BAD_REGISTRY: dict[str, dict] = {
    "rag_answer": {"version": "1.0.0", "eval_gate": True},
    "unversioned_answer": {"eval_gate": True},
    # No eval_gate key on purpose -> PR004
    "repo_stats": {"version": "1.0.0"},
    # Points at a file that does not exist -> PR002
    "legacy_summarizer": {"version": "0.9.0", "eval_gate": True},
}

# A long, expensive template: Opus pricing with a fat context. Every
# quality eval could pass; only the budget gate fails this change.
BAD_PROMPT_TEMPLATE = (
    "You are an meticulous engineering assistant. Restate the full repository "
    "architecture before answering. Include every file path you know about, "
    "repeat the user question verbatim, then answer in exhaustive detail with "
    "no regard for token cost. " * 20
)

GOOD_PROMPT_TEMPLATE = GOOD_PROMPT_FILES["rag_answer.md"]


def write_sample_pack(directory: Path, files: dict[str, str]) -> Path:
    """Write a sample prompt pack (files only) to a directory."""
    for filename, content in files.items():
        target = directory / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    return directory


# ---------------------------------------------------------------------------
# 8. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    """Audit a given prompts directory, or run the built-in demo."""
    if len(argv) > 1:
        target = Path(argv[1])
        if not target.is_dir():
            print(f"Not a directory: {target}", file=sys.stderr)
            return 2
        report = analyze_directory(target)
        print(render_audit(report))
        return 1 if report.critical_count else 0

    print("LLMOps Lifecycle Exercise 01")
    print("Prompt-registry auditor + cost budgeter (stdlib only).")
    print("Running the built-in demo against a bad pack and a good pack.")
    print("Pass a directory to audit a real one, for example:")
    print("    python exercises/01-llmops-lifecycle.py")
    print("        path/to/prompts")
    print()

    with tempfile.TemporaryDirectory(prefix="llmops-exercise-") as tmp:
        scratch = Path(tmp)
        bad_dir = write_sample_pack(scratch / "bad", BAD_PROMPT_FILES)
        good_dir = write_sample_pack(scratch / "good", GOOD_PROMPT_FILES)

        bad_report = analyze_directory(bad_dir)
        bad_report.findings = audit_registry(
            bad_report.files, registry_from_dict(BAD_REGISTRY)
        )
        bad_report.registry = registry_from_dict(BAD_REGISTRY)
        print(render_audit(bad_report))
        print()

        good_report = analyze_directory(good_dir)
        good_report.findings = audit_registry(
            good_report.files, registry_from_dict(GOOD_REGISTRY)
        )
        good_report.registry = registry_from_dict(GOOD_REGISTRY)
        print(render_audit(good_report))
        print()

        bad_cost = estimate_query_cost(
            model="claude-3-opus-20240229",
            prompt_template=BAD_PROMPT_TEMPLATE,
            context_chars=40_000,
            expected_output_tokens=2_000,
            queries_per_month=50_000,
        )
        bad_budget = Budget(per_query_usd=0.05, monthly_usd=2_000.00)
        bad_cost_findings = check_budgets(bad_cost, bad_budget)
        print(render_cost(bad_cost, bad_budget, bad_cost_findings))
        print()

        good_cost = estimate_query_cost(
            model="gpt-4o-mini",
            prompt_template=GOOD_PROMPT_TEMPLATE,
            context_chars=8_000,  # DevMate's rag_context_char_budget
            expected_output_tokens=350,
            queries_per_month=20_000,
        )
        good_budget = Budget(per_query_usd=0.01, monthly_usd=50.00)
        good_cost_findings = check_budgets(good_cost, good_budget)
        print(render_cost(good_cost, good_budget, good_cost_findings))

    total_bad = len(bad_report.findings) + len(bad_cost_findings)
    total_good = len(good_report.findings) + len(good_cost_findings)
    print("-" * 72)
    print(
        f"Demo result: bad pack raised {total_bad} findings "
        f"({bad_report.critical_count} critical, "
        f"{bad_report.warning_count} warning, {bad_report.info_count} info "
        f"from the registry audit; {len(bad_cost_findings)} from the cost "
        f"budgets); good pack raised {total_good} findings."
    )
    print("The temporary sample packs were cleaned up automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
