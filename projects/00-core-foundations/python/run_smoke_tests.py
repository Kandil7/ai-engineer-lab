"""
Python Module - Smoke Test Runner
=================================
Verifies that all .py files across the module can be compiled/parsed
without syntax errors, and that demo sections run without crashes.

Usage:
    python run_smoke_tests.py              # Run all tests
    python run_smoke_tests.py --phase 1    # Run Phase 1 only
    python run_smoke_tests.py --file 01-introduction.py  # Run single file
    python run_smoke_tests.py --list       # List all discovered files
    python run_smoke_tests.py --all --verify  # Run all with _verify()

Exit code: number of failures (0 = all passed)
"""

import argparse
import os
import subprocess
import sys
import time
import random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# Files that cannot run standalone (require stdin, special setup, etc.)
SKIP_FILES = {
    "practice_all.py",
    "practice_no_solutions.py",
    "39-pip.py",
    "40-virtualenv.py",
    "33-user-input.py",  # requires stdin
    "test_challenge.py",  # pytest file — run via `python -m pytest`, not standalone
}

# Directories to skip entirely
SKIP_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".mimocode",
    ".idea",
    "django",  # Django not installed - reference only (R7)
    "outputs",  # Exercise outputs - regenerated on run
}

# Per-file timeout in seconds (prevents hangs like R1.1)
FILE_TIMEOUT = 30

# CI reproducibility settings
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("PYTHONHASHSEED", "0")
random.seed(42)
np.random.seed(42)


def discover_files(root_dir: str) -> list[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRECTORIES]
        for f in filenames:
            if f.endswith(".py") and f not in SKIP_FILES:
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, HERE)
                files.append(rel)
    return sorted(files)


def print_header(text: str, width: int = 60) -> None:
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def smoke_test_file(rel_path: str, verify: bool = False) -> tuple[bool, str]:
    full = os.path.join(HERE, rel_path)

    # Step 1: Check syntax (explicit UTF-8 encoding)
    compile_result = subprocess.run(
        [
            sys.executable,
            "-c",
            f"import io; compile(io.open({repr(full)}, 'r', encoding='utf-8').read(), {repr(rel_path)}, 'exec')",
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if compile_result.returncode != 0:
        msg = compile_result.stderr.strip() or compile_result.stdout.strip()
        return False, f"SYNTAX ERROR: {msg[:200]}"

    # Step 2: Try running (with timeout, with UTF-8 environment)
    # Use --verify flag if requested and file supports it
    cmd = [sys.executable, full]
    if verify:
        cmd.append("--verify")

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["MPLBACKEND"] = "Agg"
        run_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=FILE_TIMEOUT,
            env=env,
        )
        if run_result.returncode != 0:
            msg = run_result.stderr.strip() or run_result.stdout.strip()
            if "Traceback" in msg or "Error" in msg:
                return False, f"RUNTIME ERROR: {msg[:200]}"
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {FILE_TIMEOUT}s (likely hang - see R1.1)"
    except subprocess.CalledProcessError as e:
        return False, f"SUBPROCESS ERROR: {e}"

    return True, "OK"


def run_phase(phase_dir: str, label: str, verify: bool = False) -> tuple[int, int, float]:
    phase_path = os.path.join(HERE, phase_dir) if phase_dir != "." else HERE
    if not os.path.isdir(phase_path):
        return 0, 0, 0.0

    files = [f for f in discover_files(phase_path) if phase_dir in f]
    if not files:
        return 0, 0, 0.0

    print_header(f"Phase: {label}  ({len(files)} files)")

    passed = 0
    failed = 0
    start = time.perf_counter()

    for f in files:
        ok, detail = smoke_test_file(f, verify=verify)
        status = "PASS" if ok else "FAIL"
        display = f.replace("\\", "/") if len(f) > 50 else f
        print(f"  [{status}] {display:<50}  {detail[:60]}")
        if ok:
            passed += 1
        else:
            failed += 1

    elapsed = time.perf_counter() - start
    return passed, failed, elapsed


def main():
    parser = argparse.ArgumentParser(description="Smoke test runner for Python learning module")
    parser.add_argument(
        "--phase", type=int, choices=range(1, 10), help="Run only a specific phase (1-9)"
    )
    parser.add_argument("--file", type=str, help="Run a single file (relative path)")
    parser.add_argument(
        "--list", action="store_true", help="List all discovered files without running"
    )
    parser.add_argument("--all", action="store_true", help="Run all phases (default)")
    parser.add_argument(
        "--verify", action="store_true", help="Pass --verify to each exercise file to run _verify()"
    )
    parser.add_argument(
        "--clean-outputs", action="store_true", help="Clean outputs/ directory before running tests"
    )
    parser.add_argument(
        "--timeout", type=int, default=30, help="Per-file timeout in seconds (default: 30)"
    )
    args = parser.parse_args()

    global FILE_TIMEOUT
    FILE_TIMEOUT = args.timeout

    if args.clean_outputs:
        import shutil

        outputs_dir = os.path.join(HERE, "outputs")
        if os.path.isdir(outputs_dir):
            shutil.rmtree(outputs_dir)
            os.makedirs(os.path.join(outputs_dir, "scipy"))
            os.makedirs(os.path.join(outputs_dir, "matplotlib"))
            os.makedirs(os.path.join(outputs_dir, "dbs"))
            print(f"Cleaned and recreated outputs/ directory")
        else:
            os.makedirs(os.path.join(outputs_dir, "scipy"))
            os.makedirs(os.path.join(outputs_dir, "matplotlib"))
            os.makedirs(os.path.join(outputs_dir, "dbs"))
            print(f"Created outputs/ directory")

    phases = [
        ("01-core-python", "01 - Core Python"),
        ("02-advanced-python", "02 - Advanced Python"),
        ("03-libraries", "03 - Libraries (NumPy, Pandas, etc.)"),
        ("04-databases", "04 - Databases (MySQL, MongoDB)"),
        ("05-web-frameworks", "05 - Web Frameworks (FastAPI, Django)"),
        ("06-data-structures-algorithms", "06 - DSA"),
        ("07-machine-learning", "07 - Machine Learning"),
        ("08-mlops", "08 - MLOps (Reproducibility to E2E)"),
        ("09-genai", "09 - GenAI (LLMs, RAG, Agents, Production)"),
    ]

    if args.list:
        print_header("Discovered Python Files")
        for phase_dir, label in phases:
            phase_path = os.path.join(HERE, phase_dir)
            if not os.path.isdir(phase_path):
                continue
            files = [f for f in discover_files(phase_path) if phase_dir in f]
            if files:
                print(f"\n  [{label}]")
                for f in files:
                    print(f"    {f}")
        return 0

    if args.file:
        print_header(f"Testing: {args.file}")
        ok, detail = smoke_test_file(args.file, verify=args.verify)
        status = "PASSED" if ok else "FAILED"
        print(f"  {status}: {detail}")
        return 0 if ok else 1

    print("=" * 60)
    print("  PYTHON MODULE - Smoke Test Suite")
    print("=" * 60)
    print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Verify mode: {'ON' if args.verify else 'OFF'}")
    print(f"  Per-file timeout: {FILE_TIMEOUT}s")
    print(f"  Skip list: {sorted(SKIP_FILES)}")
    print(f"  Skip dirs: {sorted(SKIP_DIRECTORIES)}")

    total_passed = 0
    total_failed = 0
    total_start = time.perf_counter()

    for phase_dir, label in phases:
        if args.phase:
            phase_num = int(phase_dir[:2])
            if phase_num != args.phase:
                continue
        p, f, elapsed = run_phase(phase_dir, label, verify=args.verify)
        total_passed += p
        total_failed += f

    if not args.phase:
        capstones_dir = os.path.join(HERE, "capstones")
        if os.path.isdir(capstones_dir):
            print_header("Capstones")
            for proj in sorted(os.listdir(capstones_dir)):
                proj_path = os.path.join(capstones_dir, proj)
                if os.path.isdir(proj_path):
                    py_files = [f for f in os.listdir(proj_path) if f.endswith(".py")]
                    for pf in py_files:
                        rel = f"capstones/{proj}/{pf}"
                        ok, detail = smoke_test_file(rel, verify=args.verify)
                        status = "PASS" if ok else "FAIL"
                        print(f"  [{status}] {rel:<50}  {detail[:50]}")
                        if ok:
                            total_passed += 1
                        else:
                            total_failed += 1

    total_elapsed = time.perf_counter() - total_start

    print()
    print("=" * 60)
    summary = f"  Results: {total_passed} passed, {total_failed} failed"
    if total_failed:
        summary += " [FAIL]"
    else:
        summary += " [PASS]"
    print(summary)
    print(f"  Duration: {total_elapsed:.1f}s")
    print("=" * 60)

    return total_failed


if __name__ == "__main__":
    sys.exit(main())
