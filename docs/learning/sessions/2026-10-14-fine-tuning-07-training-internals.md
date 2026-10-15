# Fine-Tuning 07 track completed: quiz + exercise validator

### Context

ai-engineer-lab, fine-tuning track 07-training-internals. Pre-compaction work created lecture and glossary; this session finished the remaining two deliverables (quiz markdown, exercise .py) and ran the full verification gate.

### Explanation

Deliverables: (1) 07-training-internals-quiz.md, 414 lines, 15 questions tagged 4 Easy / 6 Medium / 5 Hard, each with a details block containing a 2-3 sentence explanation, ending with Score Tracking and Answer Key tables (Scoring Guide placed before them so the file ends with the two named tables, per spec); nav link to 06 quiz. (2) 07-training-internals.py, 703 lines, stdlib-only validator with 8 fixed finding codes TRN001-TRN008, module-constant BAD_CONFIG (raises all 8) and GOOD_CONFIG (raises zero), VRAM breakdown, LR warmup+cosine schedule preview, JSON CLI mode with exit codes 0 (clean) / 1 (critical findings) / 2 (unreadable input). Verification evidence: py_compile exit 0; demo exit 0 with "all asserts passed"; bad pack 8 findings (7 critical, 1 warning), good pack 0; tests/repo-structure/validate.ps1 75 passed / 0 failed / 0 warnings; tests/knowledge/validate.ps1 11 passed / 0 failed; both files 0 CRLF pairs, no BOM; git status shows no pre-existing file touched by this task (whole 07-training-internals/ folder is untracked).

### Alternatives

Considered keeping the Scoring Guide after the Answer Key (template order) but the task explicitly required the file to end with Score Tracking and Answer Key, so the guide was moved before them. Considered rewriting explanations as single unwrapped lines to hit the ~346-line target exactly; chose wrapped 90-char explanations instead, landing at 414 lines (target was "~346", content-complete over exact length).

### Rationale (Why this?)

Key decisions: em dashes removed from printed runtime output only (Windows console mojibake) while allowed in md titles (all 6 sibling quizzes use "— Quiz" in H1); TRN008 message reworded to read correctly when checkpoint_metric is missing; from_dict ignores unknown JSON keys, so configs must use dataclass field names (base_params_b, trainable_frac) or defaults silently change the verdict; tests/repo-structure and tests/knowledge validators are the workspace gates relevant to new track files, both run from repo root; docs link checker only scans docs/, so projects/ links are unchecked manually instead.

### Next Steps

Remaining workspace gates for a full-repo check: prompts/workflows/templates/registries validators (not affected by this change, so not run this session). Commit left to the user.

---
