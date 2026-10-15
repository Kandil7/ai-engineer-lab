# Glossary: CI/CD Pipelines

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Workflow | One YAML file declaring triggers, jobs, and steps | Stored under `.github/workflows/` |
| Trigger | The event that starts a workflow run | push, PR, tag, cron, manual, workflow_run |
| Job | Unit of work executed on one isolated runner | Parallel unless `needs` links them |
| Step | One command or action inside a job | Steps share a filesystem; jobs do not |
| Action | Reusable step implementation referenced with `uses:` | Pin to a full commit SHA |
| Runner | The machine a job executes on | `ubuntu-latest` is a moving alias |
| needs | Job-to-job dependency edge | Implicit condition is `success()` |
| Matrix | Axis expansion of one job into N runs | `fail-fast` defaults to true |
| Cache | Best-effort store that speeds up future runs | Key it with `hashFiles` |
| Artifact | File uploaded from a run for later jobs or humans | The only filesystem bridge between jobs |
| Quality Gate | A failing step that blocks merge or deploy | Order gates cheap to expensive |
| Secret | Encrypted value injected into a run on demand | Reference via `env`, never inside `run:` |
| Environment | Named deployment target with protection rules | Required reviewers live in settings |
| Concurrency Group | Keyed lock limiting simultaneous runs | Cancel superseded branch runs |
| Reusable Workflow | A workflow called from another via `workflow_call` | The calling job sets no `runs-on` |
| workflow_run | Event fired when another workflow completes | Runs in default-branch context |
| Path Filter | `paths:` / `paths-ignore:` trigger narrowing | Can make a required check never start |
| Pinning | Freezing a dependency to immutable content | Branch refs move; SHAs do not |
| Flaky Test | A test that fails without a code change | Quarantine, do not delete |
| act | Local runner that executes jobs inside Docker | Cannot reproduce services or Windows runners |

---

## Detailed Definitions

### Workflow

**Definition:** A single YAML file that declares when a pipeline runs, what jobs it contains, and what each job executes. Workflows are independent files; one run belongs to exactly one workflow.

**Example:**
```yaml
# .github/workflows/ci.yml — the only workflow in this repository
name: CI
on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
  workflow_dispatch:

jobs:
  devmate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

**Related Terms:** Trigger, Job, Run

**Key Facts:**
- Files must live in `.github/workflows/` with a `.yml` or `.yaml` extension
- Each workflow has a `name:` shown in the Actions tab and addressable by `gh workflow run <name>`
- Workflows cannot import each other directly; share logic with reusable workflows
- The workflow file that runs is the one from the triggering ref (except `schedule` and `workflow_run`, which use the default branch)

---

### Trigger

**Definition:** An event or schedule declared in the `on:` block that causes a workflow run to be created. The trigger set, plus its branch, tag, and path filters, is the pipeline's entire activation policy.

**Example:**
```yaml
on:
  push:
    branches: [main]
    paths: ["src/**"]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 3 * * 1"
  workflow_dispatch:
  workflow_run:
    workflows: ["Build & Push"]
    types: [completed]
```

**Related Terms:** Path Filter, workflow_run, Scheduled Run

**Key Facts:**
- `pull_request` checks out a temporary merge commit; `push` checks out the pushed head
- `schedule` always executes the default branch's version of the workflow file
- `workflow_dispatch` only exists once the workflow file is on the default branch
- A trigger with `paths` skips the entire run when no changed file matches, which can strand a required check

---

### Job

**Definition:** A named unit of work that runs on one runner to completion. Jobs are the parallelism boundary: every job gets a fresh VM, a clean checkout, and no memory of sibling jobs.

**Example:**
```yaml
jobs:
  lint:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .

  test:
    needs: lint
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - run: pytest -q
```

**Related Terms:** Runner, needs, Step, Timeout

**Key Facts:**
- Without `needs`, all jobs start in parallel — free concurrency you should exploit
- A failed job skips every job that needs it, unless the dependent job overrides with `if:`
- Files written in one job do not exist in another; use artifacts
- `timeout-minutes` bounds the job; the platform default is six hours

---

### Step

**Definition:** One action or shell command inside a job. Steps run sequentially in declaration order, share the working directory and environment of the runner, and stop the job at the first non-zero exit unless the step is marked `continue-on-error`.

**Example:**
```yaml
    steps:
      - uses: actions/checkout@v4
      - name: Install the project
        run: uv sync --locked --extra dev
      - name: Lint (ruff)
        run: uv run --frozen ruff check .
        continue-on-error: false      # a gate: failure fails the job
```

**Related Terms:** Job, Action, Gate, `continue-on-error`

**Key Facts:**
- Steps in a job share a filesystem; this is the only implicit file sharing in Actions
- `run:` executes in the runner's shell; `uses:` executes someone else's action
- `if:` on a step lets later steps run conditionally without a new job
- `continue-on-error: true` turns a step into an advisory report instead of a gate

---

### Action

**Definition:** A reusable unit of step logic referenced by `uses:`, either a public action from a repository, a local composite action in the same repo, a Docker container action, or another workflow.

**Example:**
```yaml
      # Marketplace action, pinned to a full commit SHA (recommended)
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8  # v4.2.2

      # Same action pinned to a mutable major tag (convenient, mutable)
      - uses: actions/checkout@v4

      # Local composite action, no ref needed
      - uses: ./.github/actions/setup-project

      # Docker container action
      - uses: docker://alpine:3.19
```

**Related Terms:** Pinning, Composite Action, Third-Party Risk

**Key Facts:**
- Every ref-taking `uses:` should carry a ref; missing refs and `@main`/`@master` are supply-chain hazards
- A public action runs with your job's token and secrets — treat action choice as a trust decision
- Local (`./`) and `docker://` references are exempt from ref pinning rules
- Inputs arrive under `with:`; outputs are read in later steps via `steps.<id>.outputs`

---

### Runner

**Definition:** The machine a job executes on, selected by `runs-on:`. GitHub-hosted runners are ephemeral virtual machines; self-hosted runners are machines you register and maintain.

**Example:**
```yaml
    runs-on: ubuntu-24.04        # pinned image generation
    runs-on: ubuntu-latest       # moving alias, retargeted by GitHub
    runs-on: windows-2022        # needed for PowerShell suites
    runs-on: self-hosted         # your own hardware, your own patching
```

**Related Terms:** Label, Runner Image, Self-Hosted

**Key Facts:**
- `ubuntu-latest`, `windows-latest`, and `macos-latest` are aliases that change when GitHub ships a new image
- Pinning the label (`ubuntu-24.04`) trades automatic upgrades for reproducibility
- Public repositories get free hosted minutes; private repositories draw down a monthly allowance
- Self-hosted runners suit GPUs and intranet access, and inherit all patching and hardening work

---

### Job Dependency (`needs`)

**Definition:** The edge in the job graph declaring that a job must wait for others. The default satisfaction condition is `success()`, so any failed or skipped dependency skips the dependent job.

**Example:**
```yaml
jobs:
  build: { ... }
  test:
    needs: build
  package:
    needs: [build, test]              # waits for BOTH
  report:
    needs: [build, test]
    if: ${{ always() }}               # runs even when a need failed
```

**Related Terms:** Job, Condition, `if`

**Key Facts:**
- `needs` creates ordering only — it does not transfer files or environment variables
- Job outputs cross the edge explicitly: `needs.test.outputs.artifact-name`
- `${{ always() }}`, `${{ !cancelled() }}`, and `${{ failure() }}` override the implicit success condition
- An acyclic graph is required; a `needs` cycle fails workflow validation

---

### Matrix

**Definition:** A strategy that expands a single job definition into multiple runs, one per combination of the declared axis values, optionally adjusted by `include` and `exclude`.

**Example:**
```yaml
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
        os: [ubuntu-24.04, windows-2022]
        exclude:
          - os: windows-2022
            python-version: "3.11"
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

**Related Terms:** Strategy, `fail-fast`, Job

**Key Facts:**
- Each combination is a separate runner with its own log and check conclusion
- `fail-fast: true` (the default) cancels sibling legs on the first failure, hiding per-leg causes
- Fold matrix values into cache keys, or legs will read each other's caches
- `matrix` values come from static lists or `fromJSON(...)` on a dynamic string

---

### Cache

**Definition:** A best-effort, key-addressed store of files (dependency wheels, build layers) restored in later runs to avoid re-downloading or rebuilding. Correctness must never depend on a cache hit.

**Example:**
```yaml
      - uses: actions/cache@v4
        with:
          path: ~/.cache/uv
          key: uv-${{ runner.os }}-${{ hashFiles('**/uv.lock') }}
          restore-keys: uv-${{ runner.os }}-
```

**Related Terms:** Artifact, `hashFiles`, buildx `type=gha`

**Key Facts:**
- Key without `hashFiles` = permanently stale cache; keys should track the lockfile
- `restore-keys` allows prefix matches: an exact miss falls back to the nearest older cache
- Pull request caches cannot overwrite caches used by the base branch
- Docker layer caching is separate: `cache-from: type=gha` / `cache-to: type=gha,mode=max`

---

### Artifact

**Definition:** A file or set of files uploaded from a run, retained for a configured period, downloadable by later jobs in the same run and by humans from the run page. Artifacts are the only durable file hand-off between isolated jobs.

**Example:**
```yaml
      # Producer
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

      # Consumer, in a later job
      - uses: actions/download-artifact@v4
        with:
          name: coverage-report
```

**Related Terms:** Cache, Job Isolation, Retention

**Key Facts:**
- Jobs live on different machines; artifacts are how output crosses that boundary
- Artifacts are retained per repository settings, then garbage-collected
- Use caches for inputs you can rebuild, artifacts for outputs you cannot
- Artifact names must be unique within a run — which is why matrix legs append their axis values

---

### Quality Gate

**Definition:** A step or job whose non-zero exit blocks the merge or the deploy. Everything with `continue-on-error`, `|| true`, or a warning-only setting is a report, not a gate, and should be labeled as one.

**Example:**
```yaml
      - name: Lint (ruff)               # gate: exit code blocks merge
        run: uv run --frozen ruff check .
      - name: Lint (advisory)           # report: prints findings, cannot fail
        run: ruff check . --statistics || true
      - name: Eval gate
        run: uv run --frozen python -m devmate.eval.run_ragas --mode offline
             --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70
```

**Related Terms:** Step, Exit Code, Advisory Check

**Key Facts:**
- Order gates by cost: lint in seconds, tests in minutes, evals longer
- A gate with no threshold (coverage reported but not enforced) is documentation, not policy
- This repository's gates: ruff, format check, mypy, uv audit, pytest, offline eval, six validators, docs checks
- Every gate needs a clear failure message; `::error file=...::` annotations land on the PR diff

---

### Secret

**Definition:** An encrypted value stored at the repository, environment, or organization level and injected into a run only when referenced. The runner masks registered secret values in logs.

**Example:**
```yaml
      # ❌ value substituted into script text before the shell runs
      run: curl -H "Auth: ${{ secrets.API_TOKEN }}" https://api.example.com

      # ✅ value arrives as an environment variable
      env:
        API_TOKEN: ${{ secrets.API_TOKEN }}
      run: curl -H "Auth: $API_TOKEN" https://api.example.com
```

**Related Terms:** `GITHUB_TOKEN`, Environment Secret, Script Injection

**Key Facts:**
- `${{ secrets.X }}` inside `run:` expands before bash starts; `env` keeps script text clean
- Fork pull requests receive no repository secrets and a read-only token
- Masking is a log filter, not a leak barrier; it does not cover `ps`, crash dumps, or exfiltration
- Untrusted event fields interpolated into `run:` are script injection — same fix: route through `env`

---

### Environment

**Definition:** A named deployment target (development, staging, production) carrying protection rules stored in repository settings: required reviewers, wait timers, and allowed-branch policies.

**Example:**
```yaml
  deploy:
    needs: build
    runs-on: ubuntu-24.04
    environment: production     # required reviewers gate this job
    steps:
      - run: ./deploy.sh
```

**Related Terms:** Protection Rule, Required Reviewer, Manual Gate

**Key Facts:**
- Rules live in settings, not YAML — the gate cannot be removed by editing the workflow
- Environment-scoped secrets keep production credentials out of lower environments
- Deployment history per environment gives you an audit trail for rollbacks
- `projects/06-devops/ci-cd/README.md` describes the intended development/staging/production topology for this workspace

---

### Concurrency Group

**Definition:** A keyed lock over workflow runs. At most one run per group executes at a time (depending on `cancel-in-progress`), and only one pending run is kept per group.

**Example:**
```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

**Related Terms:** Cancellation, Queueing, Throttling

**Key Facts:**
- Without a group, five quick commits queue five full suites; only the last result matters
- A newer queued run replaces the older pending one in the same group
- `cancel-in-progress: true` kills the currently running job too — never enable it for deploys
- Scope the group key narrowly (workflow + ref) or unrelated runs will serialize behind each other

---

### Reusable Workflow

**Definition:** A workflow invoked from another workflow's job with `workflow_call`, so pipeline logic is defined once and shared across repositories. The calling job behaves like an action reference, not like a container job.

**Example:**
```yaml
# caller
jobs:
  test:
    uses: org/repo/.github/workflows/test-suite.yml@v1
    with:
      python-version: "3.11"
    secrets: inherit
```

**Related Terms:** `workflow_call`, Inputs, `secrets: inherit`

**Key Facts:**
- A calling job declares `uses`, `with`, `secrets`, and optionally `needs`/`if` — no `runs-on`, no `steps`
- Because the called workflow owns the runner, the calling job carries no `timeout-minutes` obligation
- Reference callees by SHA or tag, exactly like any other action
- Job statuses propagate back so the caller's downstream `needs` chain still works

---

### workflow_run

**Definition:** An event that fires when another named workflow completes, carrying the conclusion of that run. It is the sanctioned way to chain workflows, especially when the second needs privileges the first must not have.

**Example:**
```yaml
on:
  workflow_run:
    workflows: ["Build & Push"]
    types: [completed]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-24.04
    steps:
      - run: ./deploy.sh
```

**Related Terms:** Trigger, Chaining, Default-Branch Context

**Key Facts:**
- The triggered workflow runs from the default branch's workflow file, with the triggering run only as data
- It can hold secrets and write permissions even when the trigger came from an untrusted source — validate the payload
- Always gate on `conclusion == 'success'`; `completed` fires for failures too
- The example deploy chain in `projects/06-devops/ci-cd/README.md` uses exactly this pattern

---

### Path Filter

**Definition:** A trigger constraint (`paths:` or `paths-ignore:`) that starts a run only when the changed files match or do not match the given patterns.

**Example:**
```yaml
on:
  push:
    branches: [main]
    paths:
      - "projects/04-ai-engineering/devmate/**"
      - ".github/workflows/**"
  pull_request:
    paths-ignore:
      - "docs/**"
      - "**.md"
```

**Related Terms:** Trigger, Branch Protection, Sentinel Job

**Key Facts:**
- A workflow filtered out never starts — a required check then reads as missing, not green
- Documentation-only commits can skip heavy test suites; that is the main use case
- Patterns match against paths relative to the repository root
- Pair strict required checks with an always-run sentinel job if your protection rules demand a result

---

### Pinning

**Definition:** Freezing a dependency — action, runner image, container, tool version — to immutable content so the same input produces the same pipeline tomorrow. Commit SHAs pin actions; explicit versions pin tools; digests pin images.

**Example:**
```yaml
      # Unpinned (worst), mutable tag (better), SHA (correct)
      - uses: actions/checkout
      - uses: actions/checkout@main          # branch: force-push changes meaning
      - uses: actions/checkout@v4            # tag: maintainer can re-point it
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8  # v4.2.2
    runs-on: ubuntu-latest                   # moving image alias
    runs-on: ubuntu-24.04                    # fixed image generation
```

**Related Terms:** Action, Runner, Supply Chain, SHA

**Key Facts:**
- Tags are mutable strings in git; only the SHA is content-addressed
- Keep the human version in a trailing comment so updates stay reviewable
- The companion exercise encodes this as rules: `ACT001` (no ref or a branch) and `ACT002` (mutable tag)
- Pinning is a tradeoff: you must bump pins deliberately to receive fixes

---

### Flaky Test

**Definition:** A test whose outcome varies without any code change — the pipeline equivalent of a car alarm that goes off in the wind. It destroys trust in the gate faster than any missing test.

**Example:**
```bash
# Reproduce: run the suite repeatedly and count non-deterministic failures
for i in 1 2 3 4 5; do pytest -q tests/unit || echo "FAILED run $i"; done

# Isolate by marker while the cause is being fixed (this repo's pattern)
pytest -q -m "not integration and not llm"      # fast, stable gate
pytest -q -m integration                        # environment-bound, own job
```

**Related Terms:** Quarantine, Markers, Retry

**Key Facts:**
- Common causes: shared state between tests, time/timezone assumptions, unordered reads
- Quarantine = run it outside the gating job with an owner and an expiry; deleting loses coverage
- Retries mask flakiness rather than fix it; use them only to measure, not to greenwash
- This repository's integration and LLM tests are separated by pytest markers so they cannot destabilize the unit gate

---

### act

**Definition:** An open-source tool that executes GitHub Actions jobs locally inside Docker containers, using your working copy as the checkout, for fast iteration on workflow logic without pushing.

**Example:**
```bash
act -l                          # list every job the workflows expose
act -j devmate                  # run one job from the default workflow
act -W .github/workflows/ci.yml # select a specific workflow file
act -j devmate --secret API_TOKEN=...   # pass a secret the run needs
```

**Related Terms:** Runner, Local CI, Docker

**Key Facts:**
- Excellent for debugging `run:` step logic; imperfect for services, artifacts, caches, and environments
- Windows jobs (this repo's `workspace` job) are not faithfully reproducible in Docker-based `act`
- Differences from GitHub are normal — treat `act` as a fast pre-push check, not proof of CI parity
- The parity tool for this repository is `infra/scripts/local-ci.ps1`, which runs the real gates with the real local environments

---

## Summary

These terms cover the vocabulary you need to read, write, and audit a pipeline:

1. **Workflows trigger, jobs isolate, steps execute.** Almost every Actions surprise reduces to forgetting one of those three layers.
2. **The graph is `needs`; the filesystem bridge is artifacts; caches only make reruns faster.** Do not let those three roles blur.
3. **Gates are exit codes with consequences.** Reports (`|| true`, `continue-on-error`) are allowed — as long as everyone knows which is which.
4. **Untrusted content must be pinned, and secrets must stay out of script text.** SHA pins and `env` mapping are the two controls that matter most.
5. **Environments, concurrency groups, and timeouts** are the operational controls: who approves, what runs at once, and how long anything may hang.
6. **This repository's own pipeline** — five jobs, six validator suites, an offline eval gate, and the docs freshness and `-Check` drift gates — is the concrete instance of every term above.

**Next:** The companion lecture walks these concepts against `.github/workflows/ci.yml` line by line, then the exercise grades your workflow with the same static-analysis rules a reviewer would apply.
