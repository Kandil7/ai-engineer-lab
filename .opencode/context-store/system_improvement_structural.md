---
id: system_improvement_structural
reported_by: opencode
created_at: 2026-10-06T21:44:21.709Z
---

Structural batch completed 2026-10-06/07 (committed as 9f2bb41 plus working tree: current-focus task 23 + new test file). Facts: (1) cli/main.py stats split into RepoStats/collect/format/present; 4 existing tests pass unmodified = output contract preserved. (2) agent.py run split into 4 private methods; import time hoisted; no agent tests exist. (3) New tests/unit/test_api_happy_path.py: 9 tests (health/root/usage/traces/ready/ingest-404/ingest-happy/rag-query); HealthResponse carries a version field (assertion adjusted); suite 52 to 61 passed, coverage 45% to 48%. (4) Full local-ci ALL GREEN. Remaining structural debt is deeper coverage (tool dispatch, error paths) for the A2 window. Ubuntu CI runs unverified until master push.
