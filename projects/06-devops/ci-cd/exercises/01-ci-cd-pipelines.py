"""
Exercise 01: CI/CD Pipelines
============================
Analyze a GitHub Actions workflow the way a security reviewer and a CI gate
would: check action pinning, job timeouts, concurrency, runner labels, and
secrets leaking into shell script text — before a run ever starts.

This exercise is deliberately runnable without GitHub or a network. It
parses workflow YAML as text, line by line, with no third-party YAML
library, so you can run it against this repository's real pipeline at
.github/workflows/ci.yml.

Rules enforced (severity, code):
    ACT001  critical   uses: with no ref, or pinned to main/master/HEAD
    ACT002  warning    uses: pinned to a mutable tag instead of a commit SHA
    SEC001  critical   ${{ secrets.* }} interpolated into run: script text
    CFG001  warning    job declares no timeout-minutes
    CFG002  info       workflow declares no top-level concurrency group
    SUP001  warning    runs-on uses a moving *-latest runner label

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-ci-cd-pipelines.py
    python exercises/01-ci-cd-pipelines.py path/to/workflow.yml
"""

from __future__ import annotations

import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single review finding against a workflow file."""

    severity: str  # "critical" | "warning" | "info"
    code: str
    line_number: int | None
    message: str


@dataclass
class JobInfo:
    """One job block extracted from the workflow."""

    name: str
    line_number: int
    calls_reusable_workflow: bool = False
    has_timeout: bool = False
    runs_on: list[tuple[int, str]] = field(default_factory=list)


@dataclass
class Workflow:
    """Full analysis result for one workflow file."""

    path: str
    line_count: int = 0
    jobs: list[JobInfo] = field(default_factory=list)
    uses: list[tuple[int, str]] = field(default_factory=list)
    run_lines: list[tuple[int, str]] = field(default_factory=list)
    has_concurrency: bool = False
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


# ---------------------------------------------------------------------------
# 2. Parsing
# ---------------------------------------------------------------------------

# A run: key starts a block scalar (| or >) or a plain scalar that continues
# on any following line indented deeper than the key itself.
RUN_KEY_PATTERN = re.compile(r"^(\s*(?:-\s*)?)run:\s*(.*)$")
BLOCK_MARKER = re.compile(r"^[|>][+-]?$")
USES_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)")
RUNS_ON_PATTERN = re.compile(r"^\s*(?:-\s*)?runs-on:\s*(.+)$")
JOB_START_PATTERN = re.compile(r"^  ([A-Za-z0-9_-]+):\s*(?:#.*)?$")
CONCURRENCY_PATTERN = re.compile(r"^concurrency:\s*(?:#.*)?$")
JOB_TIMEOUT_PATTERN = re.compile(r"^    timeout-minutes\s*:")
SECRET_EXPRESSION = re.compile(r"\$\{\{\s*secrets\s*\.")


def indent_of(line: str) -> int:
    """Number of leading spaces on a line."""
    return len(line) - len(line.lstrip())


def find_run_blocks(
    lines: list[str],
) -> tuple[list[set[int]], list[tuple[int, str]]]:
    """Locate every `run:` key and return the script text it owns.

    Returns a list of blocked line indexes (0-based, the continuation lines
    of each run key, which no structural rule may read) and a list of
    (line_number, script text) pairs for the SEC001 secret scan. The
    continuation rule doubles as YAML plain-scalar handling, so heredoc
    bodies passed to an inline `run:` stay inside the script.
    """
    blocked: list[set[int]] = []
    run_lines: list[tuple[int, str]] = []
    i = 0
    total = len(lines)

    while i < total:
        match = RUN_KEY_PATTERN.match(lines[i])
        if not match:
            i += 1
            continue

        key_col = len(match.group(1))
        rest = match.group(2).strip()
        if rest and not BLOCK_MARKER.match(rest.split()[0]):
            run_lines.append((i + 1, rest))
        j = i + 1
        last = i
        while j < total:
            nxt = lines[j]
            if not nxt.strip():
                j += 1
                continue
            if indent_of(nxt) > key_col:
                last = j
                j += 1
            else:
                break
        for k in range(i + 1, last + 1):
            if lines[k].strip():
                run_lines.append((k + 1, lines[k]))
        blocked.append(set(range(i + 1, last + 1)))
        i = last + 1

    return blocked, run_lines


def parse_workflow(text: str) -> Workflow:
    """Parse workflow text into jobs, action refs, run scripts, and flags.

    Assumes conventional two-space YAML indentation: jobs sit at column 2
    under `jobs:`, their keys at column 4, step keys deeper still.
    """
    lines = text.splitlines()
    blocked_spans, run_lines = find_run_blocks(lines)
    blocked: set[int] = set()
    for span in blocked_spans:
        blocked |= span

    workflow = Workflow(path="", line_count=len(lines), run_lines=run_lines)
    in_jobs = False
    current: JobInfo | None = None

    for idx, line in enumerate(lines):
        if idx in blocked:
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lineno = idx + 1

        if CONCURRENCY_PATTERN.match(line):
            workflow.has_concurrency = True
            continue

        if line.startswith("jobs:"):
            in_jobs = True
            current = None
            continue

        if in_jobs and indent_of(line) == 0:
            in_jobs = False
            current = None

        if in_jobs:
            job_match = JOB_START_PATTERN.match(line)
            if job_match:
                current = JobInfo(name=job_match.group(1), line_number=lineno)
                workflow.jobs.append(current)
                continue

        uses_match = USES_PATTERN.match(line)
        if uses_match:
            workflow.uses.append((lineno, uses_match.group(1)))
            if in_jobs and current is not None and indent_of(line) == 4:
                if not line.lstrip().startswith("-"):
                    current.calls_reusable_workflow = True
            continue

        if in_jobs and current is not None:
            if JOB_TIMEOUT_PATTERN.match(line):
                current.has_timeout = True
                continue
            runs_on_match = RUNS_ON_PATTERN.match(line)
            if runs_on_match:
                current.runs_on.append((lineno, runs_on_match.group(1).strip()))

    return workflow


# ---------------------------------------------------------------------------
# 3. Rules
# ---------------------------------------------------------------------------

BRANCH_REFS = {"main", "master", "head"}
SHA40_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MUTABLE_RUNNER_PATTERN = re.compile(r"\b(?:ubuntu|windows|macos)-latest\b")


def action_ref(value: str) -> str | None:
    """The ref of a `uses:` value, '' when missing, None when not applicable.

    Local composite actions (./), Docker references (docker://), URLs, and
    expression-built references take no static ref, so no pinning rule can
    judge them.
    """
    if value.startswith(("./", "../", "docker://", "http://", "https://")):
        return None
    if "${{" in value:
        return None
    if "@" not in value:
        return ""
    return value.rsplit("@", 1)[1]


def check_unpinned_actions(workflow: Workflow, findings: list[Finding]) -> None:
    """ACT001: no ref at all, or a ref that is a movable branch."""
    for lineno, value in workflow.uses:
        ref = action_ref(value)
        if ref is None or ref == "":
            if ref == "":
                findings.append(
                    Finding(
                        severity="critical",
                        code="ACT001",
                        line_number=lineno,
                        message=(
                            f"'{value}' takes no ref. A missing ref resolves to "
                            "whatever the default branch is at run time. "
                            "Pin a full commit SHA."
                        ),
                    )
                )
        elif ref.lower() in BRANCH_REFS:
            findings.append(
                Finding(
                    severity="critical",
                    code="ACT001",
                    line_number=lineno,
                    message=(
                        f"'{value}' is pinned to the mutable branch "
                        f"'{ref}'. A force-push silently changes what "
                        "executes in this pipeline. Pin a full commit SHA."
                    ),
                )
            )


def check_mutable_action_tags(workflow: Workflow, findings: list[Finding]) -> None:
    """ACT002: pinned to a tag, which its maintainers can re-point."""
    for lineno, value in workflow.uses:
        ref = action_ref(value)
        if ref is None or ref == "":
            continue
        if ref.lower() in BRANCH_REFS:
            continue  # already reported as ACT001
        if SHA40_PATTERN.match(ref):
            continue  # content-addressed: immutable
        findings.append(
            Finding(
                severity="warning",
                code="ACT002",
                line_number=lineno,
                message=(
                    f"'{value}' is pinned to the mutable tag '{ref}'. "
                    "Tags can be re-pointed; pin the release's commit SHA "
                    "and keep the tag in a comment."
                ),
            )
        )


def check_secret_interpolation(workflow: Workflow, findings: list[Finding]) -> None:
    """SEC001: secrets expanded into script text before the shell starts."""
    for lineno, text in workflow.run_lines:
        if SECRET_EXPRESSION.search(text):
            findings.append(
                Finding(
                    severity="critical",
                    code="SEC001",
                    line_number=lineno,
                    message=(
                        "Secret interpolated into run: script text. "
                        "Map it under env: on the step and reference the "
                        "environment variable instead."
                    ),
                )
            )


def check_job_timeouts(workflow: Workflow, findings: list[Finding]) -> None:
    """CFG001: an unbounded job can hang for the six-hour platform default."""
    for job in workflow.jobs:
        if job.calls_reusable_workflow:
            continue  # the called workflow owns its own runner and timeouts
        if not job.has_timeout:
            findings.append(
                Finding(
                    severity="warning",
                    code="CFG001",
                    line_number=job.line_number,
                    message=(
                        f"Job '{job.name}' sets no timeout-minutes. "
                        "A hung step burns the six-hour default limit; "
                        "bound every job."
                    ),
                )
            )


def check_concurrency_group(workflow: Workflow, findings: list[Finding]) -> None:
    """CFG002: without a group, every push queues its own full run."""
    if not workflow.has_concurrency:
        findings.append(
            Finding(
                severity="info",
                code="CFG002",
                line_number=None,
                message=(
                    "Workflow declares no top-level concurrency group. "
                    "Superseded runs on the same ref pile up; add "
                    "concurrency: with a per-ref group and cancellation."
                ),
            )
        )


def check_runner_labels(workflow: Workflow, findings: list[Finding]) -> None:
    """SUP001: *-latest labels are aliases GitHub retargets over time."""
    for job in workflow.jobs:
        for lineno, value in job.runs_on:
            if "${{" in value:
                continue  # dynamic runner (e.g. matrix), not statically known
            if MUTABLE_RUNNER_PATTERN.search(value):
                findings.append(
                    Finding(
                        severity="warning",
                        code="SUP001",
                        line_number=lineno,
                        message=(
                            f"Job '{job.name}' runs on the moving label "
                            f"'{value}', which GitHub repoints at new images. "
                            "Pin an explicit image (ubuntu-24.04, "
                            "windows-2022)."
                        ),
                    )
                )


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze(path: Path) -> Workflow:
    """Run every rule against one workflow file."""
    text = path.read_text(encoding="utf-8")
    workflow = parse_workflow(text)
    workflow.path = str(path)

    check_unpinned_actions(workflow, workflow.findings)
    check_mutable_action_tags(workflow, workflow.findings)
    check_secret_interpolation(workflow, workflow.findings)
    check_job_timeouts(workflow, workflow.findings)
    check_concurrency_group(workflow, workflow.findings)
    check_runner_labels(workflow, workflow.findings)

    return workflow


def render(workflow: Workflow) -> str:
    """Render a human-readable report."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"GitHub Actions workflow review: {workflow.path}")
    lines.append("=" * 72)
    lines.append(
        f"Jobs: {len(workflow.jobs)}  "
        f"Action refs: {len(workflow.uses)}  "
        f"Run script lines: {len(workflow.run_lines)}"
    )
    lines.append(
        f"Findings: {workflow.critical_count} critical, "
        f"{workflow.warning_count} warning, "
        f"{workflow.info_count} info"
    )
    lines.append("")

    if not workflow.findings:
        lines.append("No findings. The workflow passes every rule in this exercise.")
        return "\n".join(lines)

    order = {"critical": 0, "warning": 1, "info": 2}
    ranked = sorted(
        workflow.findings,
        key=lambda f: (order[f.severity], f.line_number or 0),
    )
    for finding in ranked:
        location = f"L{finding.line_number}" if finding.line_number else "--"
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {location}")
        lines.append(f"             {finding.message}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample workflows used for the demo
# ---------------------------------------------------------------------------

SAMPLE_BAD = """\
name: Bad CI
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - uses: actions/setup-python@main
        with:
          python-version: "3.11"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - name: Publish
        run: |
          curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" \\
            https://example.com/publish
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "deploy ${{ secrets.GITHUB_TOKEN }}"
"""

SAMPLE_GOOD = """\
name: Good CI
on:
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8  # v4.2.2
      - uses: actions/setup-python@a1b2c3d4e5f60718293a4b5c6d7e8f9012345678
        with:
          python-version: "3.11"
      - uses: actions/cache@7c9e6679a7f4e1a6b3c1a0f1c2d3e4f5a6b7c8d9
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - name: Test
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: pytest -q
  deploy:
    needs: test
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@0f1e2d3c4b5a69788796a5b4c3d2e1f00f1e2d3c
      - run: ./scripts/deploy.sh
"""


def write_sample(path: Path, content: str) -> Path:
    """Write a sample workflow to a temporary location for analysis."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    """Analyze a given workflow file, or run the built-in demo."""
    if len(argv) > 1:
        target = Path(argv[1])
        if not target.is_file():
            print(f"Not a file: {target}", file=sys.stderr)
            return 2
        print(render(analyze(target)))
        return 0

    print("CI/CD Pipeline Exercise 01")
    print("Running the built-in demo against two sample workflows.")
    print("Pass a path to analyze a real one, for example:")
    print("    python exercises/01-ci-cd-pipelines.py")
    print("        ../../.github/workflows/ci.yml")
    print()

    with tempfile.TemporaryDirectory(prefix="workflow-exercise-") as tmp:
        scratch = Path(tmp)
        bad = write_sample(scratch / "ci-bad.yml", SAMPLE_BAD)
        good = write_sample(scratch / "ci-good.yml", SAMPLE_GOOD)

        print(render(analyze(bad)))
        print()
        print(render(analyze(good)))

        bad_workflow = analyze(bad)
        good_workflow = analyze(good)

    print("-" * 72)
    print(
        f"Demo result: bad sample raised {bad_workflow.critical_count} critical, "
        f"{bad_workflow.warning_count} warning, {bad_workflow.info_count} info "
        f"findings; good sample raised {len(good_workflow.findings)} findings."
    )
    print("The temporary samples were cleaned up automatically.")

    if good_workflow.findings:
        print("DEMO FAILED: the good sample must raise zero findings.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
