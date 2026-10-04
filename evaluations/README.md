# Evaluations System

Systematic quality assurance for all AI-assisted engineering outputs in this lab.

---

## What We Evaluate

| Category | What | Examples |
|----------|------|----------|
| **Prompts** | Prompt quality, consistency, scope control | System prompts, role prompts, critic prompts |
| **RAG** | Retrieval quality, faithfulness, completeness | Chunk strategies, embedding models, reranking |
| **Projects** | Feature completeness, code quality, test coverage | DevMate, rag-system, capstone |

## How We Evaluate

### 1. Golden Cases (Prompts)

Pre-defined input/output pairs that verify prompts produce correct, scoped results.
Each golden case has: input scenario, expected behavior, pass/fail criteria.

- Location: `evaluations/prompts/golden-cases/`
- Format: Markdown files with `## Input`, `## Expected`, `## Criteria` sections
- Run: `./infra/scripts/validate-prompts.ps1`

### 2. Regression Tests (Prompts)

Automated checks that prompt changes don't break existing behavior.
Run after any prompt modification to catch scope creep, format drift, or constraint violations.

- Location: `evaluations/prompts/regressions/`
- Format: Markdown files listing prompt ID, change description, regression checks
- Run: `./infra/scripts/validate-prompts.ps1`

### 3. RAG Metrics

Quantitative measurement of retrieval and generation quality.

| Metric | Description | Target |
|--------|-------------|--------|
| Recall@5 | % of relevant docs in top 5 results | > 0.85 |
| Precision@3 | % of top 3 results that are relevant | > 0.80 |
| Faithfulness | % of generated claims supported by context | > 0.95 |
| Answer Relevance | How well answer addresses the query | > 0.80 |

- Location: `evaluations/rag/datasets/`
- Baselines: `evaluations/rag/baselines/`
- Reports: `evaluations/rag/reports/`

### 4. Project Criteria

Per-project evaluation checklists tied to release gates.

- Location: `evaluations/projects/<project>/`
- Each project has a checklist file with pass/fail criteria
- A project is "release-ready" when all criteria pass

## Directory Structure

```text
evaluations/
  README.md                    # This file
  prompts/
    README.md                  # Prompt evaluation guide
    golden-cases/              # Golden case files
    regressions/               # Regression test files
  rag/
    README.md                  # RAG evaluation guide
    datasets/                  # Test question/answer pairs
    baselines/                 # Baseline metric snapshots
    reports/                   # Evaluation run reports
  projects/
    README.md                  # Project evaluation guide
    rag-system/                # rag-system eval criteria
    capstone/                  # capstone eval criteria
```

## How to Add Evaluations

### Adding a Prompt Golden Case

1. Create `evaluations/prompts/golden-cases/<prompt-id>-<case-name>.md`
2. Follow the template in `evaluations/prompts/README.md`
3. Run validation: `./infra/scripts/validate-prompts.ps1`

### Adding a RAG Evaluation Dataset

1. Create `evaluations/rag/datasets/<topic>-<version>.jsonl`
2. Each line: `{"question": "...", "expected_context": [...], "expected_answer": "..."}`
3. Run evaluation: documented in `evaluations/rag/README.md`

### Adding a Project Evaluation

1. Create `evaluations/projects/<project>/checklist.md`
2. List all release-gate criteria with pass/fail
3. Reference the checklist in the project's plan.md

## Running All Evaluations

```powershell
# Validate repo structure and all evals
./tests/repo-structure/validate.ps1
./tests/templates/validate.ps1
./tests/prompts/validate.ps1

# Run prompt golden cases
./infra/scripts/validate-prompts.ps1
```

## Decision Record

All evaluation-related decisions are recorded in ADRs under `docs/decisions/`.
When adding a new evaluation type or metric, create an ADR first.
