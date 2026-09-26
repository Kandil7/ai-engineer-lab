# AGENTS.md — Full-Stack AI Engineer Lab

Repo-centric learning + execution workspace. Active project: DevMate (`projects/04-ai-engineering/devmate/`).
What to work on: `docs/tracking/current-focus.md`. Plan of record: `docs/roadmap/active-track-10-week.md`.

## Verify like CI does

`make` and `pwsh` are not installed on this machine. Use `powershell` (5.1) and these
direct commands instead. Git Bash exists for shell bits.

DevMate gate — working directory `projects/04-ai-engineering/devmate/`, python at
`.venv/Scripts/python.exe`:

```powershell
& .venv/Scripts/python.exe -m ruff check .
& .venv/Scripts/python.exe -m ruff format --check .
& .venv/Scripts/python.exe -m mypy src/
& .venv/Scripts/python.exe -m pytest -q --cov=devmate --cov-report=term-missing
```

Single test: `& .venv/Scripts/python.exe -m pytest tests/unit/test_cost.py -q`. Unit tests need no API key.
`llm`-marked tests need a real key and never run in CI. No test file currently carries
the `integration` marker, so `make test-int` collects nothing; when such tests exist
they need `docker compose -f infra/docker/docker-compose.yml up -d postgres redis qdrant` first.

Workspace validators — all five must exit 0 (warnings fail the suite):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/<prompts|workflows|templates|registries|repo-structure>/validate.ps1
```

Docs gates (mirrored in CI): no broken relative links under `docs/`, and
`docs/tracking/current-focus.md` must carry a `**Last updated:**` stamp no older than 8 days.

## The `.ai` system

21 prompts in 5 layers under `.ai/prompts/`: system (2), roles (8), tasks (5),
critics (3), repair (3). Compose runs in this order: `system/workspace-governor.md`
→ role → task (optional) → `system/output-format-rules.md` → critic or repair
(optional follow-up). Never restate format rules; reuse `output-format-rules.md`.

Every prompt and workflow file carries YAML frontmatter (id, version, status, owner;
workflows also add category and entry_point) mirroring its registry entry.

21 workflows under `.ai/workflows/` in 5 tracks: feature (01-plan → 02-design →
03-build → 04-review → 05-fix → 06-reflect), debugging (01 → 04), learning (4
source workflows + source-to-exercise), architecture (3), evaluation (3).
Entry points: `feature/01-plan` for any feature, `debugging/01-symptom-capture`
for any bug. Skip `feature/02-design` unless the change touches system boundaries.

Critics second-pass and report only — they never rewrite. Repair prompts trigger
on failure modes: missing-context, over-engineering, invalid-output-shape.

Artifacts land where the workflow says: `plan.md`, `architecture-review.md`,
`ai-review.md`, `mistakes.md`, `notes.md` in the project folder;
`docs/decisions/NNNN-<slug>.md` for ADRs. Fill the matching template from
`templates/` instead of inventing a layout.

Approval checkpoints: plan approved before build, architecture approved before
large implementation, review complete before done, ADR accepted before any
irreversible change.

## Registries (`registries/`)

Six YAML inventories; they are the source of truth, not the docs:

- `prompt-registry.yaml` — all 21 prompts: id, path, version, status, layer,
  `used_by` (workflow ids or `area/*` globs), constraints.
- `workflow-registry.yaml` — all 21 workflows: `prompts_used`, template,
  produced artifacts, exit criteria.
- `template-registry.yaml` — 15 templates with required sections and `used_by`.
- `skills-registry.yaml` — 8 reusable skills; `reusable_by` must match each
  prompt's `uses_skills` in both directions.
- `decision-log.yaml` — ADR index mirroring `docs/decisions/`.
- `review-log.yaml` — review index mirroring `projects/*/ai-review.md`.

Rules: repair entries use a `trigger` with empty `used_by`.
`task.implementation-planner` is deprecated (use `role.project-planner`);
never wire a deprecated prompt into a workflow. Index scripts own their indexes
(`new-adr.ps1`, `new-review.ps1`) — don't hand-edit them.
Run `tests/registries/validate.ps1` after any prompt, workflow, or registry edit.

## PowerShell 5.1 traps on this machine

- `.ps1` files with unicode banners require a UTF-8 BOM or they fail to parse.
  `infra/scripts/*.ps1` and `tests/registries/validate.ps1` carry one deliberately.
  If you edit a script with a UTF-8 tool, re-add the BOM and re-run the script.
- Prefer temp script files plus `-File` over long inline `-Command` strings; quoting
  through the tool layer is unreliable. Scratch goes in the OS temp dir, never the repo.

## DevMate specifics

- Environment of record is `pip install -e ".[dev]"` from `pyproject.toml`. Poetry is
  not used. The venv has no `pip` — invoke everything as `python -m <tool>`.
- Local runs read `projects/04-ai-engineering/devmate/.env` (gitignored); seed it from
  `.env.example`. The `devmate.exe` console script works (`devmate stats <path>`).
- Qdrant server is pinned to v1.8.0 in compose to match client `>=1.8.0,<1.9` — don't
  bump one side without the other.
- Full `docker compose up -d` also starts `devmate-api/mcp/ui`, but `devmate/ui/` does
  not exist yet, so that service fails. Start only the infra you need (see above).
- `make eval`, `eval/run_ragas.py`, and `devmate/eval/` don't exist yet (week 2+, A3).

## Style

- Python formatting is ruff's (line-length 100, py311, 4-space). `.editorconfig` says
  2-space indent — do not reindent `.py` files to match it.
- Trailing whitespace is significant in `*.md` (editorconfig disables trimming there).
- Line endings are LF repo-wide except `*.ps1` (CRLF). Don't "fix" git's CRLF warnings.

## Pointers

- DevMate scope and review state: `projects/04-ai-engineering/devmate/plan.md`, `ai-review.md`.
- Full command reference: `MAKEFILE.md`. Golden prompt cases: `evaluations/prompts/golden-cases/`.
- Never commit secrets, `.env` files, model weights, datasets, or generated plots.
  `outputs/**/*.png` and `.coverage` are ignored; the PNGs already tracked predate the rule.
