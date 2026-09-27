# Python Lecture 02: Get Started (Install, Verify, Run)

## Topic Overview

Every environment problem in this curriculum traces back to this topic done
carelessly: the wrong interpreter, packages landing in the wrong site, PATH
missing the Scripts directory. This lecture makes installation explicit and
verifiable — download, PATH checkbox, version check, first script run — so
no later failure is ever "maybe Python is broken."

## Learning Objectives

By the end of this lecture, you will be able to:

1. Install Python from python.org with PATH configured correctly
2. Verify the interpreter (`python --version`) and locate it (`sys.executable`)
3. Run code three ways: REPL line, `python file.py`, and `python -c`
4. Diagnose "python is not recognized" as a PATH problem with a known fix
5. Distinguish `python` vs `python3` vs `py` launcher behavior on your OS

## 1. Install Once, Correctly

Download from python.org (never an app store copy you can't update), run the
installer, and check "Add Python to PATH" — the single checkbox behind most
Windows setup tickets. Verify immediately, in a NEW terminal (installers
don't retroactively fix open shells):

```bash
python --version     # Python 3.x.x — the receipt
python -c "import sys; print(sys.executable)"   # WHERE it lives, not just THAT it runs
```

## 2. Three Ways to Run

```bash
python                 # REPL: experiments and probes, history is disposable
python hello.py        # scripts: saved, repeatable, the default for coursework
python -c "print(1)"   # one-liners: probes and checks, quoting carefully
```

Coursework always means scripts: rerunnable, committable, reviewable. The
REPL is for questions ("what does this return?"), never for deliverables.

## 3. The Two Classic Failures

"python is not recognized" means PATH, not Python: re-run the installer with
the checkbox, or add the install dir plus `Scripts/` manually, then open a
new terminal. `python` opening the Microsoft Store means an app-execution
alias intercepting the name: disable the alias or use `py`. Both have
five-minute fixes once diagnosed — and both are diagnosed, not reinstalled
around.

## Common Mistakes

- Old terminal after install (PATH changes need new shells).
- `pip install X` then `import X` failing: different interpreter than pip's.
- Editing code in one folder, running a stale copy elsewhere (always `cd` first, use absolute paths in tooling).

## Course Connection

`sys.executable` from this lecture is the answer to every later "which
Python" question: venv creation, tool configuration, CI matrices, and the
smoke-test runner all resolve to one explicit interpreter. Verify first,
build second — the habit this whole track assumes.

## Key Takeaways

1. PATH checkbox, new terminal, version receipt.
2. Scripts for work, REPL for questions, `-c` for probes.
3. "Not recognized" is PATH; diagnose, don't reinstall.
