"""
Unit tests for Phase 1 basic Python examples (01-41).
Verifies the files execute without errors and produce expected output.
"""

import subprocess
import sys
from pathlib import Path
import pytest

from tests.unit.helpers import PROJECT_ROOT, discover_phase_files, run_py_file

PHASE1_FILES = discover_phase_files("01-core-python")


@pytest.mark.unit
@pytest.mark.parametrize("filepath", PHASE1_FILES, ids=lambda p: p.name)
def test_phase1_example_runs(filepath):
    """Test that each Phase 1 example file executes without errors."""
    result = run_py_file(filepath, timeout=60)
    assert result.returncode == 0, f"{filepath.name} failed: {result.stderr[:300]}"


@pytest.mark.unit
def test_introduction_output():
    """Test 01-introduction.py produces expected output (per-topic layout)."""
    file_path = (
        PROJECT_ROOT / "01-core-python" / "basics" / "01-introduction" / "01-introduction.py"
    )
    result = run_py_file(file_path, timeout=30)
    assert "Hello, World!" in result.stdout
    assert "Python is versatile and beginner-friendly!" in result.stdout
    assert "Five is greater than two!" in result.stdout
    assert "a = 4" in result.stdout
    assert "A = 5" in result.stdout


@pytest.mark.unit
def test_practice_all_imports():
    """Test that practice_all.py can be imported."""
    result = subprocess.run(
        [sys.executable, "-c", "import practice_all; print('OK')"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(PROJECT_ROOT / "01-core-python" / "practice"),
    )
    assert result.returncode == 0, result.stderr[:200]


@pytest.mark.unit
def test_practice_no_solutions_imports():
    """Test that practice_no_solutions.py can be imported."""
    result = subprocess.run(
        [sys.executable, "-c", "import practice_no_solutions; print('OK')"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(PROJECT_ROOT / "01-core-python" / "practice"),
    )
    assert result.returncode == 0, result.stderr[:200]
