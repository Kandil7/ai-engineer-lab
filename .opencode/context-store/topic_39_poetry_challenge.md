---
id: topic_39_poetry_challenge
reported_by: opencode
created_at: 2026-10-05T17:44:40.325Z
---

Topic 39-Poetry complete in projects/00-core-foundations/python/02-advanced-python/ (repo: ai-engineer-lab).

STRUCTURE (verified by directory scan): every Phase-2 topic carries exactly one quiz. Topics 01-34 keep it in the topic dir and their challenge dirs (21-34) have no quiz.md; topics 35-38 have NO topic-dir quiz and carry quiz.md inside the challenge dir instead. Topic 39 has a topic-dir quiz (39-poetry-quiz.md) and its challenge has no quiz.md, matching the 01-34 pattern. PRACTICE_SPEC wants a challenge quiz; repo practice overrides for 39.

FILES: topic dir (committed at HEAD f5d8283): 39-poetry.py, -lecture.md, -glossary.md, -quiz.md. Uncommitted new: challenges/39-poetry/{README.md,starter.py,solution.py,test_challenge.py}. Uncommitted edits: 02-advanced-python/README.md, challenges/README.md, python/README.md, learning_path.md, SKILLS_MASTERY_MAP.md, docs/roadmap/{skills-matrix,progress-dashboard}.md, plus prior-session cosmetics in the lecture/glossary.

CHALLENGE CONTRACT: tests load starter by default and solution only via env CHALLENGE_USE_SOLUTION="1" (35-38 convention; challenge 27 uses the older CHALLENGE_MODULE). Bronze expand_constraint -> (lower, upper) pairs; Silver install_closure with CountingStr comparison budget 10*n over a 2000-node chain whose root is LAST in the list; Gold audit_manifest returns fresh/groups/unsatisfied/direct_size_mb/total_size_mb/fetches with an IndexDouble fake index that raises on duplicate fetch. Measured evidence: naive scan = 2,001,000 comparisons vs 20,000 budget (fails); indexed walk passes; solution 30/30, starter 30 failed.

ENV FACTS (verified this session): ruff sees tomllib as third-party under target py310, so import tomllib must sit in its own block after a blank line, and mypy (python_version 3.10) needs `import tomllib  # type: ignore[import-not-found]` (same as 39-poetry.py). mypy on any DIRECTORY fails project-wide with `exclude */venv/* is an invalid regular expression` under mypy 2.3.1 - pre-existing, reproduces on challenge 35; run mypy on files instead. mypy on any file importing pytest also hits a numpy stub `type statement` syntax error - identical baseline on 35's test file. run_smoke_tests.py supports --file <relative path>; test_challenge.py is in its SKIP_FILES. Workspace validators: all five tests/<name>/validate.ps1 exit 0. Docs gates: relative-link scan under docs/ plus current-focus.md stamp <=8 days (2026-09-30).
