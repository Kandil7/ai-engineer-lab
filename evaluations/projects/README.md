# Project Evaluation Guide

How to evaluate project readiness and enforce release gates.

---

## Why Evaluate Projects?

Each project in this lab must meet quality standards before it is considered
"release-ready." Evaluation prevents partial implementations from being marked
complete and ensures consistency across phases.

## Per-Project Criteria

Every project gets a `checklist.md` in its evaluation directory. The checklist
defines release-gate criteria that must ALL pass.

### Standard Criteria (All Projects)

| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | Plan exists and is complete | `plan.md` has MVP, file structure, acceptance criteria |
| 2 | Architecture reviewed | `architecture-review.md` exists with no open Critical |
| 3 | Code compiles/builds | `python -m pytest` / `ruff check` succeeds |
| 4 | Tests pass | `pytest` — 0 failures |
| 5 | Code reviewed | `ai-review.md` exists with severity ratings |
| 6 | No Critical/High findings open | All Critical and High items resolved in `mistakes.md` |
| 7 | Daily log exists | `docs/learning/notes/` has reflection for this feature |

### Phase-Specific Criteria

| Phase | Additional Criteria |
|-------|-------------------|
| P0 (Foundations) | All templates exist, all registries valid |
| P1 (Core MVP) | DevMate answers a question end-to-end |
| P2 (Reliability) | Learning workflow runs end-to-end on real source |
| P3 (Scale) | infra scripts work, repo validation passes |
| P4 (Advanced) | RAG eval baseline exists, capstone builds |

## How to Create Project Evaluations

### 1. Create the Checklist

```markdown
# Evaluation Checklist: <project-name>

## Release Gate Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Plan complete | [ ] | plan.md exists |
| 2 | Architecture reviewed | [ ] | architecture-review.md |
| 3 | Code builds | [ ] | `python -m pytest` output |
| 4 | Tests pass | [ ] | `pytest` output |
| 5 | Code reviewed | [ ] | ai-review.md |
| 6 | No open Critical/High | [ ] | mistakes.md |
| 7 | Daily log exists | [ ] | docs/learning/notes/ |

## Custom Criteria
<!-- Add project-specific criteria here -->

## Sign-off
- [ ] All criteria pass
- [ ] Reviewed by: <name>
- [ ] Date: <date>
```

### 2. Populate the Checklist

For each criterion:
1. Check if the evidence exists
2. Run the verification command
3. Record the result (pass/fail) and evidence
4. If fail, create a task to fix it

### 3. Run the Evaluation

```powershell
# Validate project structure
./tests/repo-structure/validate.ps1

# For DevMate specifically
cd projects/04-ai-engineering/devmate
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m ruff check .
```

## Release Gates

A project is "release-ready" when:
1. All standard criteria pass
2. All phase-specific criteria pass
3. All custom criteria pass
4. A human reviews and signs off

### Gate Workflow

```text
Project Complete
    ↓
Create checklist.md
    ↓
Run verification commands
    ↓
Record evidence for each criterion
    ↓
All pass? → Sign off → Done
    ↓ (if any fail)
Create tasks for failures
    ↓
Fix failures
    ↓
Re-verify
```

## Evaluation Report

After evaluation, create a report in the project directory:

```markdown
# Evaluation Report: <project-name> — <date>

## Summary
- Total criteria: 7
- Passed: 7
- Failed: 0
- Status: RELEASE-READY

## Evidence
| Criterion | Status | Evidence |
|-----------|--------|----------|
| ... | ... | ... |

## Decision
- [x] Release-ready
- [ ] Not ready — see failures above
```

## Tracking Evaluation History

Each project should maintain evaluation history in its directory:

```text
projects/<project>/
  checklist.md              # Current checklist
  evaluation-reports/       # Historical reports
    2026-06-26.md
    2026-07-03.md
```

## Common Failure Patterns

| Failure | Fix |
|---------|-----|
| Plan missing acceptance criteria | Rewrite plan with concrete checkable criteria |
| No architecture review | Run architecture workflow before coding |
| Tests fail | Fix tests or update test expectations |
| Open Critical findings | Address all Critical items before sign-off |
| No daily log | Write reflection even if brief |
