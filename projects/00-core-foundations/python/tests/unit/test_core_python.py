"""
Unit tests for Python Core Foundations - Phase 1 exercises.
Tests that key exercise files compile, that the module structure is intact,
and that the smoke-test runner and dev tooling work.
"""

import subprocess
import sys
import pytest
from pathlib import Path

from tests.unit.helpers import PROJECT_ROOT, discover_phase_files

HERE = PROJECT_ROOT
SKIP_FILES = {"practice_all.py", "practice_no_solutions.py", "39-pip.py", "40-virtualenv.py"}


def _discover_phase_files(phase_dir: str) -> list[Path]:
    """Discover all topic .py files in a phase directory (recursive).

    Topics moved from a flat layout into per-topic subdirectories
    (e.g. ``01-core-python/functions/38-file-handling/38-file-handling.py``),
    so discovery is recursive and excludes non-topic trees.
    """
    phase_path = HERE / phase_dir
    if not phase_path.is_dir():
        return []
    exclude_dirs = {
        "challenges",
        "practice",
        "lectures",
        "supplementary",
        "tests",
        "lab",  # scratch exercise files, not topic demos
        "__pycache__",
    }
    files = []
    for f in sorted(phase_path.rglob("*.py")):
        if f.name in SKIP_FILES or f.name == "__init__.py":
            continue
        if any(part in exclude_dirs for part in f.relative_to(phase_path).parts[:-1]):
            continue
        files.append(f)
    return files


def _compile_check(filepath: Path) -> tuple[bool, str]:
    """Check that a Python file compiles without syntax errors."""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                f"compile(open({str(filepath)!r}, 'r', encoding='utf-8').read(), {str(filepath.name)!r}, 'exec')",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return False, result.stderr.strip()[:200]
        return True, "OK"
    except subprocess.TimeoutExpired:
        return True, "OK (timeout)"
    except Exception as e:
        return False, str(e)


# =========================================================================
# Phase 1: Core Python - Syntax Verification
# =========================================================================

PHASE1_FILES = _discover_phase_files("01-core-python")


@pytest.mark.parametrize("filepath", PHASE1_FILES, ids=lambda p: p.name)
def test_phase1_compiles(filepath):
    """Every Phase 1 file must compile without syntax errors."""
    ok, msg = _compile_check(filepath)
    assert ok, f"{filepath.name} failed to compile: {msg}"


@pytest.mark.parametrize(
    "filepath",
    [f for f in PHASE1_FILES if f.name != "__init__.py"],
    ids=lambda p: p.name,
)
def test_phase1_has_docstring(filepath):
    """Every Phase 1 exercise must have a module-level docstring."""
    content = filepath.read_text(encoding="utf-8")
    assert content.lstrip("\ufeff").startswith('"""') or content.lstrip("\ufeff").startswith(
        "'''"
    ), f"{filepath.name} missing module docstring"


def test_phase1_all_files_present():
    """Verify all core Python topic files exist (recursive layout).

    Topics 01–52 live in per-topic subdirectories; 39/40 are skipped
    (pip/virtualenv cannot run standalone).
    """
    expected = {f"{i:02d}" for i in range(1, 53)} - {"39", "40"}
    actual = {f.stem[:2] for f in PHASE1_FILES if f.stem[:2].isdigit()}
    missing = expected - actual
    assert not missing, f"Missing files: {sorted(missing)}"


# =========================================================================
# Phase 2: Advanced Python - Syntax Verification
# =========================================================================

PHASE2_FILES = _discover_phase_files("02-advanced-python")


@pytest.mark.parametrize("filepath", PHASE2_FILES, ids=lambda p: p.name)
def test_phase2_compiles(filepath):
    """Every Phase 2 file must compile without syntax errors."""
    ok, msg = _compile_check(filepath)
    assert ok, f"{filepath.name} failed to compile: {msg}"


@pytest.mark.parametrize(
    "filepath",
    [f for f in PHASE2_FILES if f.name != "__init__.py"],
    ids=lambda p: p.name,
)
def test_phase2_has_docstring(filepath):
    """Every Phase 2 exercise must have a module-level docstring."""
    content = filepath.read_text(encoding="utf-8")
    assert content.lstrip("\ufeff").startswith('"""'), f"{filepath.name} missing module docstring"


# =========================================================================
# Phase 6: DSA - Syntax Verification
# =========================================================================

PHASE6_FILES = _discover_phase_files("06-data-structures-algorithms")


@pytest.mark.parametrize("filepath", PHASE6_FILES, ids=lambda p: p.name)
def test_phase6_compiles(filepath):
    """Every DSA file must compile without syntax errors."""
    ok, msg = _compile_check(filepath)
    assert ok, f"{filepath.name} failed to compile: {msg}"


# =========================================================================
# Phase 7: ML - Syntax Verification
# =========================================================================

PHASE7_FILES = _discover_phase_files("07-machine-learning")


@pytest.mark.parametrize("filepath", PHASE7_FILES, ids=lambda p: p.name)
def test_phase7_compiles(filepath):
    """Every ML file must compile without syntax errors."""
    ok, msg = _compile_check(filepath)
    assert ok, f"{filepath.name} failed to compile: {msg}"


# =========================================================================
# Smoke Test Runner Tests
# =========================================================================


def test_smoke_runner_list_flag():
    """Smoke test runner --list must discover files."""
    result = subprocess.run(
        [sys.executable, str(HERE / "run_smoke_tests.py"), "--list"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "Discovered Python Files" in result.stdout
    assert "01-core-python" in result.stdout
    assert "02-advanced-python" in result.stdout


# =========================================================================
# Structure Validation Tests
# =========================================================================


def test_expected_directories_exist():
    """Verify all expected phase and sub-directories exist."""

    # Capstone dirs live under "projects/" in older snapshots and "capstones/"
    # in the current structure - accept either layout.
    def _any(*paths: str) -> bool:
        return any((HERE / p).is_dir() for p in paths)

    expected = [
        "01-core-python",
        "02-advanced-python",
        "03-libraries/numpy",
        "03-libraries/pandas",
        "03-libraries/matplotlib",
        "03-libraries/scipy",
        "04-databases/postgresql",
        "04-databases/mongodb",
        "05-web-frameworks/fastapi",
        "05-web-frameworks/django",
        "06-data-structures-algorithms",
        "07-machine-learning",
        "supplementary/quizzes",
        "supplementary/interviews",
        "tests/unit",
    ]
    # Dev-tooling dir: either scripts/ or _dev/ is acceptable.
    assert _any("scripts", "_dev"), "No dev-tooling directory (scripts/ or _dev/)"
    # Capstone dirs: accept projects/ or capstones/ layouts.
    for name in [
        "01-calculator",
        "02-file-manager",
        "03-api-server",
        "04-data-analyzer",
        "05-ml-pipeline",
    ]:
        assert _any(f"projects/{name}", f"capstones/{name}"), f"Capstone {name} not found"
    missing = [d for d in expected if not (HERE / d).is_dir()]
    assert not missing, f"Missing directories: {missing}"


def test_readme_exists_in_phase_dirs():
    """Verify README.md exists in all phase directories."""
    phases = [
        "01-core-python",
        "02-advanced-python",
        "03-libraries",
        "04-databases",
        "05-web-frameworks",
        "06-data-structures-algorithms",
        "07-machine-learning",
    ]
    missing = [phase for phase in phases if not (HERE / phase / "README.md").is_file()]
    for lib in ["numpy", "pandas", "matplotlib", "scipy"]:
        if not (HERE / "03-libraries" / lib / "README.md").is_file():
            missing.append(f"03-libraries/{lib}")
    assert not missing, f"Missing README.md: {missing}"


def test_requirements_txt_parses():
    """requirements.txt must be parseable."""
    req_path = HERE / "requirements.txt"
    assert req_path.is_file(), "requirements.txt not found"
    lines = req_path.read_text(encoding="utf-8").splitlines()
    deps = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
    assert len(deps) > 5, "Too few dependencies listed"


# =========================================================================
# Supplementary Content Verification
# =========================================================================


def test_quizzes_exist():
    """Verify quiz files exist (directly under supplementary/quizzes)."""
    quiz_dir = HERE / "supplementary/quizzes"
    assert quiz_dir.is_dir()
    md_files = list(quiz_dir.glob("*.md"))
    assert len(md_files) >= 25, f"Expected 25+ quizzes, found {len(md_files)}"


def test_interviews_exist():
    """Verify interview files exist (directly under supplementary/interviews)."""
    interview_dir = HERE / "supplementary/interviews"
    assert interview_dir.is_dir()
    md_files = list(interview_dir.glob("*.md"))
    assert len(md_files) >= 14, f"Expected 14+ interviews, found {len(md_files)}"


def test_phase1_lectures_exist():
    """Verify Phase 1 lecture files exist (recursive per-topic layout).

    Lectures moved from a central ``lectures/`` dir into each topic
    directory; count them recursively.
    """
    lecture_files = list((HERE / "01-core-python").rglob("*-lecture.md"))
    assert len(lecture_files) >= 40, f"Expected 40+ lecture files, found {len(lecture_files)}"


# =========================================================================
# No Stale Artifact Files Test
# =========================================================================


def test_no_stale_artifact_files():
    """Verify no stale err.txt or e.txt files exist in the module root."""
    assert not (HERE / "err.txt").is_file(), "err.txt still exists at module root"
    assert not (HERE / "01-core-python/err.txt").is_file(), "err.txt still exists"
    assert not (HERE / "01-core-python/e.txt").is_file(), "e.txt still exists"
