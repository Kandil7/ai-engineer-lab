# Lecture 01: CI/CD Pipelines with GitHub Actions

## Topic Overview

A CI/CD pipeline is the factory floor of a software project. Every push is assembled, tested, scanned, and either promoted or rejected by rules that no one can quietly skip. GitHub Actions expresses that factory in YAML: triggers decide when work starts, jobs decide what runs where, and gates decide whether the result ships. This lecture builds the model from the ground up — triggers through job graphs, matrices, caches, quality gates, secrets, environments, concurrency, reusable workflows, and runners — then grounds every concept in the real pipeline this repository runs on every push: `.github/workflows/ci.yml`, whose five jobs gate the DevMate service, the workspace registry validators, the docs freshness stamp, and the legacy curriculum suite.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Git basics, command-line comfort, a GitHub account, Docker containerization fundamentals (the Docker track's Lecture 01)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Choose** the right trigger for a pipeline, from push and pull request to tags, cron schedules, manual dispatch, and cross-workflow events
2. **Structure** a workflow as a job graph with `needs`, conditional execution, and matrix builds
3. **Separate** caches from artifacts and place each where it actually belongs
4. **Design** quality gates that fail fast: lint, format, types, tests, dependency audit, and eval metrics
5. **Handle** secrets so they reach the process environment but never the script text or the logs
6. **Protect** deployments with environments, required reviewers, and manual approval gates
7. **Bound** every run with concurrency groups, cancellation, and job timeouts
8. **Compose** reusable workflows with `workflow_call` instead of copy-pasting pipeline logic
9. **Pin** actions, runners, and images so tomorrow's build means what today's build meant
10. **Diagnose** a failing run from its logs, annotations, and exit codes
11. **Reproduce** pipeline gates locally with `act` and this repository's `local-ci.ps1`
12. **Quarantine** flaky tests so they inform without blocking the merge queue

---

## Key Concepts

### 1. The Pipeline Model

Continuous integration means every change is integrated and verified against the mainline within minutes of being written. Continuous delivery and deployment extend that verification to the artifact: build it, scan it, promote it through environments. The pipeline is the machine that enforces both.

| Term | Meaning | Question it answers |
|---|---|---|
| **Workflow** | One YAML file of triggers, jobs, and steps | What runs, and when? |
| **Run** | One execution of a workflow, created by an event | Did this particular push pass? |
| **Job** | A unit of work on one runner; jobs run in parallel unless linked | Where does this work execute? |
| **Step** | One command or action inside a job, sequentially | What exactly ran? |
| **Gate** | A step whose non-zero exit blocks everything downstream | Is this good enough to ship? |
| **Artifact** | A file uploaded from a run for another job or for humans | What did this run produce? |

```
   event (push / PR / tag / cron / manual)
                    │
                    ▼
        ┌───────────────────────┐
        │      workflow run     │   one execution, one log stream
        └───────────┬───────────┘
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 ┌─────────┐  ┌──────────┐  ┌──────────┐
 │  lint   │  │   test   │  │   docs   │   parallel by default
 └────┬────┘  └────┬─────┘  └────┬─────┘
      └────────────┼─────────────┘
                   ▼
        ┌─────────────────────┐
        │ package  (needs: …) │   runs only if every need succeeded
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │ deploy   (environment + required reviewers)
        └─────────────────────┘
```

Two properties of this model decide most design questions:

- **Jobs are isolated.** Each job gets a fresh virtual machine and a clean checkout. Nothing written in the `lint` job exists in the `test` job unless you upload an artifact and download it. Steps inside one job share a filesystem; jobs do not.
- **Failure propagates down the graph.** A failed job marks every job that `needs` it as skipped. Gates therefore belong as early in the graph as possible, so a broken lint fails in seconds instead of after a twenty-minute test matrix.

### 2. Triggers and Filters

The `on:` block is the only reason a workflow ever runs. Choosing the wrong trigger is the most common source of pipelines that never fire, or fire far too often.

```yaml
name: CI
on:
  push:                          # a commit landed on a branch
    branches: [main]
    paths: ["src/**"]            # run only when these paths changed
  pull_request:                  # a PR targets a branch; merge ref is checked out
    branches: [main]
  schedule:
    - cron: "0 3 * * 1"          # Mondays 03:00 UTC; default branch only
  workflow_dispatch:             # manual, from the UI or `gh workflow run`
    inputs:
      version:
        required: true
  workflow_run:                  # fires when another workflow finishes
    workflows: ["Build & Push"]
    types: [completed]
```

| Trigger | Typical use | The gotcha |
|---|---|---|
| `push` | Validate and deploy branches you own | Fires on every commit; combine with `paths` or `concurrency` |
| `pull_request` | Validate proposed changes | Checks out the temporary merge commit, not your branch head |
| `push: tags` | Build and release versioned artifacts | Tag pushes do not trigger branch `push` workflows |
| `schedule` | Nightly dependency audits, stale-report jobs | Always executes the workflow file from the default branch |
| `workflow_dispatch` | Human-triggered runs with inputs | Requires the workflow file to already exist on the default branch |
| `workflow_run` | Chain workflows: build, then deploy | Runs in the default branch's context with a privileged token; never wire it to untrusted fork output |

Facts that matter in practice:

- **`push` vs `pull_request`.** Use `pull_request` to validate community contributions (the token is read-only for forks). Use `push` for your own branches and for deployment. A workflow with both triggers double-runs on same-repo PR branches unless you scope the branches apart.
- **Path filters skip the whole workflow.** With `paths:`, a docs-only commit never starts the run at all, so a "required" check can show as missing rather than green. Branch protection needs `paths-ignore`-aware rules or a always-run sentinel job.
- **This repository's real triggers.** `.github/workflows/ci.yml` fires on `push` and `pull_request` targeting `master`, plus `workflow_dispatch` (lines 10-15). Note the branch is `master` here, not `main`; `projects/06-devops/ci-cd/README.md` shows `main` in its illustrative examples, and examples in that README are partly aspirational — always trust the workflow file itself.

### 3. Job Graphs: `needs` and Conditions

Jobs with no `needs` run in parallel — GitHub's default is your free parallelism, and wasting it is a scheduling mistake. `needs` builds the dependency graph.

```yaml
jobs:
  lint:
    runs-on: ubuntu-24.04
    steps: [ ... ]

  unit:
    needs: lint                 # skipped entirely if lint failed

  package:
    needs: [lint, unit]         # runs only after BOTH succeed
    if: ${{ !cancelled() }}

  report:
    needs: [lint, unit]
    if: ${{ always() }}         # runs even on failure, for summaries
```

- `needs: [a, b]` waits for all of them, and the implicit condition is `success()` — any failed or skipped need skips the dependent job.
- `if: ${{ always() }}` (or `!cancelled()`) overrides that; required when a reporting or cleanup job must run after failures.
- **File transfer between jobs needs artifacts.** `actions/upload-artifact` in the producer, `actions/download-artifact` in the consumer. The runner filesystem does not carry over.
- `outputs:` and `needs.<job>.outputs` pass small values (strings) across the graph; files never pass that way.

### 4. Matrix Builds

A matrix expands one job definition into N runs — the standard way to test multiple Python versions, operating systems, or dependency sets without duplicating YAML.

```yaml
  test:
    needs: lint
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false                 # report ALL failures, not just the first
      max-parallel: 2                  # cap concurrency on limited runners
      matrix:
        os: [ubuntu-24.04, windows-2022]
        python-version: ["3.11", "3.12"]
        include:
          - os: ubuntu-24.04
            python-version: "3.13"     # add one extra combination
        exclude:
          - os: windows-2022
            python-version: "3.13"     # drop one combination
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

- Each combination is a separate runner, separate log, separate status check. GitHub renders them as one check with per-leg detail.
- **`fail-fast` defaults to `true`**: the first red leg cancels its siblings. That saves minutes but hides whether the failure is Python-version-specific or universal. Turn it off while debugging, on once the suite is stable.
- Matrix legs share cache names unless you fold the matrix values into the cache key — otherwise version A's wheel cache is served to version B.
- A matrix of one is still a valid matrix; `fromJSON` lets you build the axis dynamically from a JSON string or a file.

### 5. Caching and Artifacts

These two storage features are constantly conflated. They differ in scope, lifetime, and intent.

| | **Cache** | **Artifact** |
|---|---|---|
| Purpose | Speed up future runs (dependencies, build layers) | Carry output between jobs or to humans |
| Lifetime | Best-effort; evicted under LRU and size limits | Retained for a configured number of days |
| Scope | Readable across branches per GitHub's scoping rules; PRs can read base-branch caches, never write them | Downloadable by any job in the same run, and from the run page |
| Keyed by | `key` + `restore-keys` prefix matching | Name |
| Miss behavior | Rebuild or re-download; never correctness-critical | Download fails; correctness-critical |

```yaml
      # Dependency cache: keyed on the lockfile, not on a static string
      - uses: actions/cache@v4
        with:
          path: ~/.cache/uv
          key: uv-${{ runner.os }}-${{ hashFiles('**/uv.lock') }}
          restore-keys: uv-${{ runner.os }}-

      # Build output for the next job in THIS run: an artifact
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
```

- **A cache key without `hashFiles` is a stale-cache bug.** The cache hits forever, serving last month's dependencies after the lockfile changed.
- Docker builds use a different cache backend: `docker/build-push-action` with `cache-from: type=gha` and `cache-to: type=gha,mode=max` stores buildx layer cache in GitHub's cache service. `projects/06-devops/ci-cd/README.md` shows exactly this pattern in its example build workflow.
- Caches are a performance optimization, never a correctness mechanism. A pipeline that passes only because of a cache hit will fail on a cold run — which is what a weekly scheduled run with an empty cache is for.

### 6. Quality Gates

A gate is any step whose failure blocks the merge or the deploy. The ordering principle: **run the cheapest gate first**, so most failures surface in seconds.

This repository's real gate sequence, taken from the `devmate` job in `.github/workflows/ci.yml`:

| # | Gate | Command | Fails when |
|---|---|---|---|
| 1 | Lint | `uv run --frozen ruff check .` | Any non-advisory lint rule fires |
| 2 | Format | `uv run --frozen ruff format --check .` | A file would be reformatted |
| 3 | Types | `uv run --frozen mypy src/` | A type error exists in `src/` |
| 4 | Audit | `uv audit --locked --no-extra eval --no-extra agents` | A vulnerable dependency sits in the audited set |
| 5 | Tests | `uv run --frozen pytest -q --cov=devmate --cov-report=term-missing` | Any test fails |
| 6 | Eval | `uv run --frozen python -m devmate.eval.run_ragas --mode offline --no-report --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70` | Offline Hit@5 < 1.0 or MRR < 0.70 |

Three design decisions visible in that table:

- **Gates are ordered fast to slow.** Ruff fails in under a second; the pytest suite takes minutes. Placing lint first means most broken pushes never reach the expensive steps.
- **Coverage is reported, not gated.** The pytest step passes `--cov=devmate --cov-report=term-missing`, which prints coverage but does not fail on a threshold. That is a deliberate posture, not an oversight — the gate that would block a merge on coverage numbers is a separate policy decision (`--cov-fail-under=`). The coverage-threshold table in `projects/06-devops/ci-cd/README.md` is an example of target policy, not something `ci.yml` currently enforces.
- **Some steps are advisory by design.** The `legacy-lint` job runs `ruff check . --statistics || true` — it prints roughly 2.3k style findings across teaching files but cannot fail the build; the job's `pytest -q` run is the actual gate. An `|| true` step is a report, never a gate, and should be labeled as such in the step name.

Beyond tests, a full quality-gate inventory for an AI service also includes: dependency audit (present), secret scanning, container image scanning (from the Docker track), and retrieval/eval metrics (present as the offline RAG gate).

### 7. Secrets Handling

GitHub stores secrets at the repository or environment level and injects them on demand. The failure mode is not storage — it is substitution.

```yaml
      # ❌ BAD: the secret value is substituted into the SCRIPT TEXT before bash runs
      - name: Publish
        run: curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" https://api.example.com

      # ✅ GOOD: the secret becomes an environment variable; the script text never contains it
      - name: Publish
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com
```

Why the difference is real, not stylistic:

- `${{ }}` expressions are expanded by the runner **before** the shell starts, so the raw value exists in the command string handed to the process — visible in `ps` output on self-hosted runners, in error traces, and in any `set -x` transcript.
- Environment variables keep the script text clean. The runner masks registered secret values in logs, but masking is a log filter, not a leak prevention mechanism.
- **Script injection is the same bug with untrusted input.** Interpolating `${{ github.event.issue.title }}` or any event field an outsider controls directly into `run:` gives that outsider shell execution. Map it to `env` and reference the variable.
- Least privilege applies to the default token too: declare `permissions: { contents: read }` at workflow level so a compromised step cannot push code or mint packages.
- Fork pull requests receive a read-only token and **no repository secrets** — by design. A workflow that needs secrets on PRs must be `pull_request_target`-based or triggered post-merge, both of which require careful review.

### 8. Environments and Manual Gates

GitHub Environments pair a deployment target with protection rules. The rules live in repository settings, not in YAML, which is the point: an approver cannot be skipped by editing the workflow.

```yaml
  deploy-production:
    needs: build
    runs-on: ubuntu-24.04
    environment: production          # protection rules apply here
    steps:
      - run: ./deploy.sh
```

| Mechanism | What it enforces | Typical use |
|---|---|---|
| Required reviewers | A named human clicks Approve before the job starts | Production deploys |
| Wait timer | Fixed cooling-off period between start and execution | Coordinated rollouts |
| Deployment branch policy | Only tags or `main` may deploy from this environment | Production |
| Job `environment:` key | Binds a job to all of the above | Any privileged job |

`projects/06-devops/ci-cd/README.md` describes a three-environment design — development, staging, production with a manual gate — as the intended topology for this workspace. Today only `ci.yml` exists under `.github/workflows/`; the build, deploy, and environment layers described in that README are a design target, not live configuration. The manual-gate primitive itself has two entry points: the environment's required reviewers, and `workflow_dispatch`, where a human decides to run the workflow at all.

### 9. Concurrency and Cancellation

Without a concurrency group, every push queues its own run: five quick commits produce five full test suites, the last one being the only result that matters.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

- The group key scopes exclusivity — per workflow and ref above, which serializes runs on the same branch.
- GitHub keeps at most one pending run per group: a newer queued run replaces the older pending one. Runs already executing are left alone unless `cancel-in-progress` is true.
- **Cancel PR and branch-validation runs freely; never cancel deploys or tag builds.** The expression form above makes cancellation ref-aware, so a merge to `main` is never half-killed.
- A workflow without any `concurrency` key — including this repository's current `ci.yml` — relies entirely on GitHub's per-repository queue. Fine at small scale; it is the first thing to add when runs start stacking.

### 10. Reusable Workflows and `workflow_call`

A reusable workflow is a workflow called from another workflow as if it were an action. It is the answer to copy-pasted pipeline logic across repositories.

```yaml
# .github/workflows/test-suite.yml  (the callee)
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      API_TOKEN:
        required: true

jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: pytest -q
```

```yaml
# .github/workflows/ci.yml  (the caller)
jobs:
  test:
    uses: org/repo/.github/workflows/test-suite.yml@v1   # or ./.github/workflows/… locally
    with:
      python-version: "3.11"
    secrets: inherit
```

- A job with `uses:` is a **call**, not a container: it declares no `runs-on` and no `steps`. The called workflow owns the runners and steps. (The static analyzer in this lecture's exercise exempts such jobs from the timeout rule for exactly this reason.)
- Reusable workflows must be referenced by ref — a SHA or tag, not a branch, for the same pinning reasons as any other action.
- `secrets: inherit` passes the caller's secrets implicitly; explicit `secrets:` mapping is tighter.
- Inputs and outputs are typed with `type: string | number | boolean | object`, and the called workflow's job statuses propagate back to the caller's `needs`.

### 11. Runners: Cloud, Self-Hosted, and Local (`act`)

The runner is the machine a job executes on. The label in `runs-on:` selects it.

| Runner | `runs-on:` value | Tradeoff |
|---|---|---|
| GitHub-hosted Linux | `ubuntu-24.04` (pinned) or `ubuntu-latest` (moving alias) | Free minutes on public repos, no maintenance, ephemeral |
| GitHub-hosted Windows | `windows-2022` or `windows-latest` | Required for PowerShell suites, `.ps1` with CRLF, and Windows-path behavior |
| GitHub-hosted macOS | `macos-14` or `macos-latest` | Expensive minutes; only for Apple-targeted builds |
| Self-hosted | `self-hosted` plus your own labels | Your hardware (GPU boxes, intranet), but you patch, secure, and scale it |

- **`ubuntu-latest` is a moving alias** — GitHub retargets it when a new LTS image ships, silently changing preinstalled tool versions. Pin `ubuntu-24.04` when the toolchain matters; this repository's `ci.yml` currently uses `ubuntu-latest` and `windows-latest`, which is the mutable-label tradeoff: convenience over reproducibility.
- This workspace's `workspace` job deliberately runs on `windows-latest` because the six `tests/*/validate.ps1` suites are PowerShell and the repo's line-ending rules make Windows the honest execution environment.
- **`act` runs workflow jobs locally inside Docker**: `act -l` lists jobs, `act -j devmate` runs one. It is excellent for debugging step logic, and it cannot reproduce services, artifacts, caches, environments, or Windows runners faithfully.
- The closest local ground truth for this repo is `infra/scripts/local-ci.ps1`, which mirrors the `ci.yml` gates using the environments of record:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/local-ci.ps1
```

It runs the DevMate ruff/mypy/pytest/eval gates, the legacy curriculum suite, all six workspace validators, the two generated-file `-Check` gates, and `infra/scripts/docs-gates.ps1`, printing `LOCAL CI: ALL GREEN` on success.

### 12. Flaky-Test Quarantine

A flaky test — one that passes and fails without a code change — poisons the gate: after two false alarms, developers re-run failed CI instead of reading it, and the pipeline stops meaning anything.

- **Separate by marker first.** This repository's DevMate suite already splits its suite by pytest markers: default local runs exclude integration and LLM tests (`-m 'not integration and not llm'` via addopts), unit tests run in the `devmate` job, and `-m integration` runs against real Qdrant and Redis service containers in the `integration` job. Slower, more environment-dependent tests fail in their own job instead of discrediting the unit gate.
- **Retry at the job level, loudly.** `timeout-minutes` plus an explicit retry action makes a hang distinguishable from a failure. A bare re-run button hides both.
- **Quarantine, do not delete.** A quarantined test runs in a scheduled or non-gating job, still reported, with an owner and an expiry date for the quarantine. Deleting it loses the coverage; letting it gate loses the signal.
- **Diagnose before excusing.** The usual root causes are shared state between tests, time and timezone assumptions, and unordered network or database reads. Fixing the cause is cheaper in perpetuity than paying a retry tax on every run.

### 13. This Repository's Real CI: The Five Jobs and the Docs Gates

`.github/workflows/ci.yml` is the only workflow under `.github/workflows/`. Its shape:

| Job | Runner | What it gates |
|---|---|---|
| `devmate` | `ubuntu-latest` | ruff lint + format, mypy, uv dependency audit, pytest with coverage, offline eval gate (Hit@5 ≥ 1.0, MRR ≥ 0.70) |
| `workspace` | `windows-latest` | Six `tests/*/validate.ps1` suites: prompts, workflows, templates, registries, knowledge, repo-structure |
| `integration` | `ubuntu-latest` | `pytest -m integration` against `qdrant/qdrant:v1.8.0` and `redis:7-alpine` service containers |
| `docs` | `ubuntu-latest` | Broken relative links under `docs/` and the `current-focus.md` freshness stamp |
| `legacy-lint` | `ubuntu-latest` | Advisory ruff report plus the real gate, `pytest -q`, over `projects/00-core-foundations/python/` |

The `docs` job deserves close study, because it is three different gate patterns in one job.

**Gate 1 — broken relative links.** The step walks every `*.md` under `docs/` (excluding `docs/plan/archive/`), extracts Markdown links with `grep -oE '\]\([^)#][^)]*\.md[^)]*\)'`, strips anchors, skips `http*` targets, and tests each relative target with `[ -f "$dir/$link" ]`. A miss emits a GitHub error annotation — `::error file=$file::broken link -> $link` — and fails the job, so the broken link appears inline on the pull request instead of in a scrollback log.

**Gate 2 — the freshness stamp.** `docs/tracking/current-focus.md` must carry a `**Last updated:** YYYY-MM-DD` stamp, and the stamp may be at most 8 days old:

```bash
stamp=$(grep -oE '\*\*Last updated:\*\* [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
age=$(( ( $(date +%s) - $(date -d "$stamp" +%s) ) / 86400 ))
if [ "$age" -gt 8 ]; then exit 1; fi
```

A missing stamp fails immediately; a stale stamp fails with the age printed. The comment in the workflow records why: the file went five weeks stale under the previous plan, and this gate makes staleness impossible to ignore. The local twin is `infra/scripts/docs-gates.ps1`, which runs both docs gates outside CI.

**Gate 3 — generated-file drift checks.** Two committed files are generated from registries, and CI refuses to let them drift:

| Script | Flag | Source of truth | Generated view it protects |
|---|---|---|---|
| `infra/scripts/build-knowledge-index.ps1` | `-Check` | `registries/knowledge-registry.yaml` | `docs/reference/INDEX.md` |
| `infra/scripts/build-skills-scoreboard.ps1` | `-Check` | `registries/evidence.yaml` plus the knowledge registry | `docs/roadmap/skills-scoreboard.md` |

The pattern is **generate, commit, verify**: authors regenerate locally and commit the result; CI re-runs the generator in check mode and fails if the committed file no longer matches what the generator would produce. Nobody hand-edits generated views, and nobody can forget to regenerate one.

---

## Code Examples

### Example 1: A Complete PR Validation Workflow

```yaml
name: PR Validation
on:
  pull_request:
    branches: [main]

concurrency:
  group: pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v4.2.2
      - uses: astral-sh/setup-uv@<40-char-sha>
        with:
          enable-cache: true
      - run: uv sync --locked --extra dev
      - run: uv run --frozen ruff check .
      - run: uv run --frozen ruff format --check .

  test:
    needs: lint
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8   # v4.2.2
      - uses: actions/setup-python@<40-char-sha>
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@<40-char-sha>
        with:
          path: ~/.cache/uv
          key: uv-${{ runner.os }}-py${{ matrix.python-version }}-${{ hashFiles('**/uv.lock') }}
          restore-keys: uv-${{ runner.os }}-py${{ matrix.python-version }}-
      - run: uv run --frozen pytest -q --cov=devmate --cov-report=xml
      - uses: actions/upload-artifact@<40-char-sha>
        with:
          name: coverage-${{ matrix.python-version }}
          path: coverage.xml
```

Every `<40-char-sha>` placeholder stands for the full commit SHA of the tagged release, with the human-readable version in a trailing comment. GitHub's own hardening guidance and the OpenSSF Scorecard both check for exactly this.

### Example 2: Tag-Triggered Build with an Environment Gate

```yaml
name: Release
on:
  push:
    tags: ["v*"]

concurrency:
  group: release-${{ github.ref }}
  cancel-in-progress: false          # never kill a release mid-flight

jobs:
  build:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@<40-char-sha>
      - uses: docker/setup-buildx-action@<40-char-sha>
      - uses: docker/login-action@<40-char-sha>
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@<40-char-sha>
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    environment: production            # required reviewers live in settings
    steps:
      - uses: actions/checkout@<40-char-sha>
      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: ./scripts/deploy.sh
```

This is an illustrative pattern — this repository has no release workflow yet, and `ci.yml` is the only file under `.github/workflows/`. The buildx `type=gha` cache flags and the tag trigger come from the example in `projects/06-devops/ci-cd/README.md`, shown here with pinning, timeouts, and the environment gate added.

### Example 3: Diagnosing a Failed Run with the `gh` CLI

```bash
# 1. Recent runs of the real CI workflow, newest first
gh run list --workflow ci.yml --limit 10

# 2. Per-job status and conclusion for one run
gh run view <run-id>

# 3. Only the failed job's log — not the megabytes of green
gh run view <run-id> --log-failed

# 4. Live-watch a run you just triggered (ci.yml has workflow_dispatch)
gh workflow run ci.yml

# 5. Check states on a PR, including the docs job's annotations
gh pr checks <pr-number>
```

The reading order matters: job conclusions first (which gate failed), then the failed job's log (the `::error` annotations name the exact file and line), then re-run locally with `local-ci.ps1` if the failure reproduces outside GitHub.

---

## Common Mistakes to Avoid

### 1. Interpolating Secrets into `run:`

```yaml
# ❌ BAD: the token is substituted into the script text before the shell runs
run: curl -H "Auth: ${{ secrets.API_TOKEN }}" https://api.example.com

# ✅ GOOD: the token travels as an environment variable
env:
  API_TOKEN: ${{ secrets.API_TOKEN }}
run: curl -H "Auth: $API_TOKEN" https://api.example.com
```

### 2. Pinning Actions to Branches or Not at All

```yaml
# ❌ BAD: a force-push to main silently changes what executes in your pipeline
- uses: actions/checkout
- uses: actions/setup-python@main

# ✅ GOOD: the exact commit, forever, with the tag kept as a human comment
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8  # v4.2.2
```

### 3. Leaving Jobs Unbounded

```yaml
# ❌ BAD: a hung test burns the six-hour default job limit and every runner minute
jobs:
  test:
    runs-on: ubuntu-latest

# ✅ GOOD: a hang becomes a fast, obvious failure
jobs:
  test:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
```

### 4. Cache Keys Without a Content Hash

```yaml
# ❌ BAD: serves the same cache forever, regardless of lockfile changes
key: uv-${{ runner.os }}

# ✅ GOOD: invalidated exactly when dependencies change
key: uv-${{ runner.os }}-${{ hashFiles('**/uv.lock') }}
```

### 5. Assuming Files Survive Between Jobs

```yaml
# ❌ BAD: the next job starts on a fresh VM with an empty filesystem
- run: pytest --cov=xml
# next job: coverage.xml is gone

# ✅ GOOD: artifacts bridge jobs; caches only accelerate them
- uses: actions/upload-artifact@<sha>
  with: { name: coverage, path: coverage.xml }
```

### 6. Deploying Without an Environment Gate

```yaml
# ❌ BAD: any push to any branch reaches the deployment step
on: push
jobs:
  deploy: { runs-on: ubuntu-latest, steps: [ { run: ./deploy.sh } ] }

# ✅ GOOD: tags only, manual approval in front, bounded and cancel-safe
on:
  push: { tags: ["v*"] }
jobs:
  deploy:
    environment: production
    timeout-minutes: 15
    steps: [ { run: ./deploy.sh } ]
```

---

## Best Practices

1. **Pin every action to a full commit SHA**, keeping the release tag in a trailing comment
2. **Pin runner labels** (`ubuntu-24.04`) whenever preinstalled tool versions affect results
3. **Order gates cheap to expensive** so most failures surface in seconds
4. **Set `timeout-minutes` on every job**; treat a missing timeout as a defect
5. **Add a workflow-level `concurrency` group** and cancel superseded branch runs
6. **Key caches with `hashFiles`** of the lockfile, never a static string
7. **Pass secrets through `env`**, never through `${{ }}` inside `run:`
8. **Grant `permissions:` explicitly**, defaulting to `contents: read`
9. **Deploy through `environment:`** with required reviewers for anything irreversible
10. **Separate test classes with markers** so slow or environment-bound suites gate on their own
11. **Keep generated files verified with `-Check`** instead of trusting human diligence
12. **Run the pipeline locally before pushing** with `local-ci.ps1` or `act -j <job>`

---

## Practice Exercises

### Exercise 1: Read Your Own Pipeline
Run `gh run list --workflow ci.yml --limit 5`, pick a run, and use `gh run view <run-id> --log-failed` to identify which of the five jobs failed and which gate inside it produced the error. If every run is green, break a docs link on a branch and watch the `docs` job catch it.

### Exercise 2: Add What `ci.yml` Is Missing
Draft (on a scratch branch, not a merge) the three smallest hardening changes the real workflow needs: `timeout-minutes` on all five jobs, a top-level `concurrency` group, and pinned runner labels. Estimate the minutes saved by cancellation on a busy branch day.

### Exercise 3: Build a Matrix Gate
Write a two-leg matrix workflow over Python 3.11 and 3.12 that runs `pytest -q`, with `fail-fast: false`, a lockfile-hashed cache key, and coverage uploaded as an artifact. Verify with `act -l` that `act` sees both legs.

### Exercise 4: Local-to-CI Parity
Run `powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/local-ci.ps1` and compare its gate list to `.github/workflows/ci.yml`. Name one gate that runs locally but not in CI, or vice versa, and explain why the asymmetry exists.

### Exercise 5: Static-Analysis Your Workflows
Run the companion exercise against the real pipeline:

```powershell
cd projects\06-devops\ci-cd
python exercises\01-ci-cd-pipelines.py ..\..\..\.github\workflows\ci.yml
```

Then explain every finding it raises: which are genuine hardening gaps, which are policy tradeoffs, and what you would fix first.

---

## Summary

CI/CD is where engineering discipline becomes mechanical. The durable takeaways:

1. **Triggers are a design decision.** Push validates, tags release, cron audits, `workflow_run` chains — and path filters and branch scoping decide how often the factory actually runs.
2. **Jobs are isolated machines; `needs` is the only graph.** Parallel by default, failure propagates downward, artifacts are the only filesystem bridge.
3. **Caches accelerate, artifacts transport.** A cache key without `hashFiles` is a bug waiting for next month's lockfile.
4. **Gates run cheap to expensive and fail loud.** This repo's sequence — lint, format, types, audit, tests, eval metrics — plus the advisory `|| true` report that is explicitly not a gate.
5. **Secrets belong in `env`, approvals belong in `environments`, bounds belong in `timeout-minutes` and `concurrency`.** Each control has exactly one correct home.
6. **The docs gates are the pattern to remember:** a broken-link scan, a freshness stamp, and two generated files protected by `-Check` — proof that a pipeline can gate documentation quality with the same rigor as code.

**Next lecture:** Deployment pipelines — promoting built artifacts through environments with health-gated rollouts, rollback, and the CD half of the story, starting from `projects/06-devops/deployment/README.md`.
