"""
Exercise 01: Docker Containerization
====================================
Analyze a Dockerfile the way a reviewer and a CI gate would: count layers,
detect cache-ordering mistakes, and flag security problems before an image
ever gets built.

This exercise is deliberately runnable without Docker installed. It parses
Dockerfiles as text and applies the rules from Lecture 01, so you can run it
against any Dockerfile in this repository, including the real one at
projects/04-ai-engineering/devmate/docker/Dockerfile.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-containerization.py
    python exercises/01-containerization.py path/to/Dockerfile
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
class Instruction:
    """One parsed Dockerfile instruction."""

    raw: str
    keyword: str
    arguments: str
    line_number: int
    is_exec_form: bool


@dataclass
class Finding:
    """A single review finding against a Dockerfile."""

    severity: str  # "critical" | "warning" | "info"
    code: str
    line_number: int | None
    message: str


@dataclass
class Analysis:
    """Full analysis result for one Dockerfile."""

    path: str
    instructions: list[Instruction] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def layer_count(self) -> int:
        """Instructions that produce a filesystem layer."""
        producing = {"RUN", "COPY", "ADD"}
        return sum(1 for i in self.instructions if i.keyword in producing)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Parsing
# ---------------------------------------------------------------------------

INSTRUCTION_PATTERN = re.compile(
    r"^\s*(FROM|RUN|CMD|LABEL|MAINTAINER|EXPOSE|ENV|ADD|COPY|ENTRYPOINT|"
    r"VOLUME|USER|WORKDIR|ARG|ONBUILD|STOPSIGNAL|HEALTHCHECK|SHELL)\s+(.*)$",
    re.IGNORECASE,
)


def strip_continuations(text: str) -> str:
    """Collapse backslash line continuations into single logical lines."""
    return re.sub(r"\\\s*\n", " ", text)


def strip_comments(text: str) -> str:
    """Remove full-line comments while preserving line count."""
    lines = text.splitlines()
    return "\n".join("" if line.lstrip().startswith("#") else line for line in lines)


def is_exec_form(arguments: str) -> bool:
    """True when arguments are a JSON array, i.e. the exec form."""
    return arguments.strip().startswith("[")


def parse_dockerfile(text: str) -> list[Instruction]:
    """Parse Dockerfile text into instructions, preserving line numbers."""
    logical = strip_continuations(strip_comments(text))
    instructions: list[Instruction] = []

    for line_number, line in enumerate(logical.splitlines(), start=1):
        match = INSTRUCTION_PATTERN.match(line)
        if not match:
            continue
        instructions.append(
            Instruction(
                raw=line.strip(),
                keyword=match.group(1).upper(),
                arguments=match.group(2).strip(),
                line_number=line_number,
                is_exec_form=is_exec_form(match.group(2)),
            )
        )

    return instructions


# ---------------------------------------------------------------------------
# 3. Rules
# ---------------------------------------------------------------------------

SECRET_PATTERN = re.compile(
    r"(api[_-]?key|secret|password|token|passwd)\s*=\s*\S+", re.IGNORECASE
)
UNPINNED_FROM = re.compile(r"^FROM\s+(\S+)$", re.IGNORECASE)


def check_root_user(instructions: list[Instruction], findings: list[Finding]) -> None:
    """A container that never sets USER runs as root."""
    has_user = any(i.keyword == "USER" for i in instructions)
    if not has_user:
        findings.append(
            Finding(
                severity="critical",
                code="SEC001",
                line_number=None,
                message="No USER instruction. The container process will run as root.",
            )
        )
        return

    last_user = [i for i in instructions if i.keyword == "USER"][-1]
    if last_user.arguments.strip().lower() in {"root", "0", "0:0"}:
        findings.append(
            Finding(
                severity="critical",
                code="SEC002",
                line_number=last_user.line_number,
                message=f"USER is set to '{last_user.arguments}'. Run as an unprivileged user.",
            )
        )


def check_cmd_form(instructions: list[Instruction], findings: list[Finding]) -> None:
    """Shell-form CMD and ENTRYPOINT swallow SIGTERM."""
    for inst in instructions:
        if inst.keyword in {"CMD", "ENTRYPOINT"} and not inst.is_exec_form:
            findings.append(
                Finding(
                    severity="warning",
                    code="RUN001",
                    line_number=inst.line_number,
                    message=(
                        f"{inst.keyword} uses the shell form. "
                        "Use the exec form so the process is PID 1 and receives SIGTERM."
                    ),
                )
            )


MANIFEST_NAMES = {
    "pyproject.toml",
    "uv.lock",
    "poetry.lock",
    "requirements.txt",
    "requirements-dev.txt",
    "setup.py",
    "setup.cfg",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "go.mod",
    "go.sum",
    "cargo.toml",
    "cargo.lock",
    "gemfile",
    "gemfile.lock",
    "pipfile",
    "pipfile.lock",
}


def copy_sources(arguments: str) -> list[str]:
    """Source operands of a COPY/ADD instruction, excluding the destination."""
    tokens = arguments.split()
    if len(tokens) < 2:
        return []
    sources = tokens[:-1]
    return [s for s in sources if not s.startswith("--")]


def is_manifest_only(instruction: Instruction) -> bool:
    """True when every copied file is a dependency manifest.

    Copying only manifests before an install RUN is the recommended cache
    pattern, not a mistake. Copying application source is what invalidates
    the install layer.
    """
    sources = copy_sources(instruction.arguments)
    if not sources:
        return False
    return all(Path(s).name.lower() in MANIFEST_NAMES for s in sources)


def check_copy_order(instructions: list[Instruction], findings: list[Finding]) -> None:
    """COPY of source before an install RUN invalidates the dependency layer."""
    first_copy: Instruction | None = None
    first_run_after_copy: Instruction | None = None

    for inst in instructions:
        if inst.keyword in {"COPY", "ADD"} and first_copy is None:
            first_copy = inst
        if (
            first_copy is not None
            and inst.keyword == "RUN"
            and first_run_after_copy is None
        ):
            first_run_after_copy = inst

    if first_copy is None or first_run_after_copy is None:
        return

    if is_manifest_only(first_copy):
        return

    install_hints = ("pip", "uv ", "poetry", "npm", "apt", "apk", "cargo", "go ")
    args = first_run_after_copy.arguments.lower()
    if not any(hint in args for hint in install_hints):
        return

    # A project self-install reads the source it just copied, so the ordering
    # is mandatory rather than a mistake. Examples: `pip install .`,
    # `uv sync`, `poetry install`. Only dependency-only installs are
    # supposed to run before the source copy.
    self_install = re.search(
        r"(?:pip|uv\s+pip|poetry)\s+install\s+(?:-\S+\s+)*(?:\./?|\.\s|$)"
        r"|\buv\s+sync\b"
        r"|\bpoetry\s+install\b",
        args,
    )
    if self_install:
        return

    findings.append(
        Finding(
            severity="warning",
            code="PERF001",
            line_number=first_copy.line_number,
            message=(
                "COPY/ADD at line "
                f"{first_copy.line_number} precedes the install RUN at line "
                f"{first_run_after_copy.line_number}. Copy dependency manifests "
                "and install before copying source, or every source edit "
                "re-runs the install."
            ),
        )
    )


def check_baked_secrets(
    instructions: list[Instruction], findings: list[Finding]
) -> None:
    """Secrets written into RUN or ENV end up in image layers or history."""
    for inst in instructions:
        if inst.keyword in {"RUN", "ENV", "ARG"} and SECRET_PATTERN.search(inst.raw):
            findings.append(
                Finding(
                    severity="critical",
                    code="SEC003",
                    line_number=inst.line_number,
                    message=(
                        f"{inst.keyword} appears to embed a credential. "
                        "Inject secrets at runtime via --env-file, a secret manager, "
                        "or a BuildKit secret mount."
                    ),
                )
            )


def check_unpinned_base(
    instructions: list[Instruction], findings: list[Finding]
) -> None:
    """latest and bare tags make builds non-reproducible."""
    for inst in instructions:
        if inst.keyword != "FROM":
            continue
        args = inst.arguments
        if " as " in args.lower():
            args = re.split(r"\s+[Aa][Ss]\s+", args, maxsplit=1)[0]
        match = UNPINNED_FROM.match(args.strip())
        if not match:
            continue
        image = match.group(1)
        if image.lower() == "scratch":
            continue
        if image.endswith(":latest") or ":" not in image.split("@")[0]:
            findings.append(
                Finding(
                    severity="warning",
                    code="SUP001",
                    line_number=inst.line_number,
                    message=(
                        f"Base image '{image}' is unpinned. "
                        "Pin an explicit tag, and a digest in production."
                    ),
                )
            )


def check_healthcheck(instructions: list[Instruction], findings: list[Finding]) -> None:
    """Services that listen on a port should declare a HEALTHCHECK."""
    exposes = [i for i in instructions if i.keyword == "EXPOSE"]
    has_health = any(i.keyword == "HEALTHCHECK" for i in instructions)
    if exposes and not has_health:
        findings.append(
            Finding(
                severity="info",
                code="OPS001",
                line_number=exposes[0].line_number,
                message=(
                    "EXPOSE is declared but no HEALTHCHECK is set. "
                    "Without one, depends_on: service_healthy cannot gate on readiness."
                ),
            )
        )


def check_wasteful_copy(
    instructions: list[Instruction], findings: list[Finding]
) -> None:
    """COPY . . before a .dockerignore is the classic context blow-up."""
    for inst in instructions:
        if inst.keyword in {"COPY", "ADD"} and re.match(
            r"^\.(\s|\s*$)", inst.arguments
        ):
            findings.append(
                Finding(
                    severity="warning",
                    code="PERF002",
                    line_number=inst.line_number,
                    message=(
                        "COPY/ADD of the entire context ('.'). Confirm .dockerignore "
                        "excludes .git, virtualenvs, caches, .env files, and model weights."
                    ),
                )
            )
            break


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze(path: Path) -> Analysis:
    """Run every rule against one Dockerfile."""
    text = path.read_text(encoding="utf-8")
    instructions = parse_dockerfile(text)
    analysis = Analysis(path=str(path), instructions=instructions)

    check_root_user(instructions, analysis.findings)
    check_cmd_form(instructions, analysis.findings)
    check_copy_order(instructions, analysis.findings)
    check_baked_secrets(instructions, analysis.findings)
    check_unpinned_base(instructions, analysis.findings)
    check_healthcheck(instructions, analysis.findings)
    check_wasteful_copy(instructions, analysis.findings)

    return analysis


def render(analysis: Analysis) -> str:
    """Render a human-readable report."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"Dockerfile review: {analysis.path}")
    lines.append("=" * 72)
    lines.append(
        f"Instructions: {len(analysis.instructions)}  "
        f"Layers (RUN/COPY/ADD): {analysis.layer_count}"
    )
    lines.append(
        f"Findings: {analysis.critical_count} critical, "
        f"{analysis.warning_count} warning, "
        f"{len(analysis.findings) - analysis.critical_count - analysis.warning_count} info"
    )
    lines.append("")

    if not analysis.findings:
        lines.append("No findings. The Dockerfile passes every rule in this exercise.")
        return "\n".join(lines)

    order = {"critical": 0, "warning": 1, "info": 2}
    for finding in sorted(analysis.findings, key=lambda f: order[f.severity]):
        location = f"L{finding.line_number}" if finding.line_number else "--"
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {location}")
        lines.append(f"             {finding.message}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample Dockerfiles used for the demo
# ---------------------------------------------------------------------------

SAMPLE_BAD = """\
FROM python:3.12
ENV OPENAI_API_KEY=sk-live-example-12345
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD uvicorn app:app --host 0.0.0.0
"""

SAMPLE_GOOD = """\
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev
COPY src/ ./src/

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
RUN useradd --system --uid 10001 appuser
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0"]
"""


def write_sample(path: Path, content: str) -> Path:
    """Write a sample Dockerfile to a temporary location for analysis."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    """Analyze a given Dockerfile, or run the built-in demo."""
    if len(argv) > 1:
        target = Path(argv[1])
        if not target.is_file():
            print(f"Not a file: {target}", file=sys.stderr)
            return 2
        print(render(analyze(target)))
        return 0

    print("Docker Containerization Exercise 01")
    print("Running the built-in demo against two sample Dockerfiles.")
    print("Pass a path to analyze a real one, for example:")
    print("    python exercises/01-containerization.py")
    print("        ../../04-ai-engineering/devmate/docker/Dockerfile")
    print()

    with tempfile.TemporaryDirectory(prefix="dockerfile-exercise-") as tmp:
        scratch = Path(tmp)
        bad = write_sample(scratch / "Dockerfile.bad", SAMPLE_BAD)
        good = write_sample(scratch / "Dockerfile.good", SAMPLE_GOOD)

        print(render(analyze(bad)))
        print()
        print(render(analyze(good)))

        bad_analysis = analyze(bad)
        good_analysis = analyze(good)

    print("-" * 72)
    print(
        f"Demo result: bad sample raised {bad_analysis.critical_count} critical "
        f"and {bad_analysis.warning_count} warning findings; "
        f"good sample raised {good_analysis.critical_count} critical "
        f"and {good_analysis.warning_count} warning findings."
    )
    print("The temporary samples were cleaned up automatically.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
