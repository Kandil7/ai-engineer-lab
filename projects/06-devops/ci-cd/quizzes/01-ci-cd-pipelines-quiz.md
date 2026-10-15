# Quiz 01: CI/CD Pipelines

## Topic Overview
This quiz covers GitHub Actions pipeline fundamentals: triggers and filters, job graphs with `needs`, matrix builds, caching versus artifacts, quality gates, secret handling, environments and manual gates, concurrency and cancellation, reusable workflows, runner pinning, and the docs gates this repository's real `ci.yml` enforces.

---

## Questions

### Question 1
**What does every job in a GitHub Actions run start with?**

- A) A fresh runner with a clean checkout, isolated from the other jobs
- B) The filesystem state left behind by the previously finished job
- C) A shared network mount holding all other jobs' workspaces
- D) Only the artifacts downloaded from upstream jobs

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Each job receives its own ephemeral runner and a fresh checkout. Nothing written during one job exists in another unless it is uploaded as an artifact and downloaded later. Steps inside a single job share a filesystem; jobs never do.
</details>

---

### Question 2
**When a job fails, what happens to jobs that list it in `needs`?**

- A) They run immediately in parallel to save time
- B) They run with a warning annotation on the pull request
- C) They are skipped, because the implicit condition on a `needs` edge is `success()`
- D) They run only the steps marked `if: always()`

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `needs` carries an implicit `success()` condition, so a failed or skipped dependency skips every dependent job. Reporting or cleanup jobs that must run after failures override this explicitly with `if: ${{ always() }}` or `${{ !cancelled() }}`.
</details>

---

### Question 3
**Why is mapping a secret through `env:` safer than interpolating `${{ secrets.X }}` directly inside `run:`?**

- A) Environment variables are encrypted at rest on the runner disk
- B) `env:` values are invisible to every process in the step
- C) Secrets in `run:` are automatically masked, so both forms are equivalent
- D) `${{ }}` is expanded into the script text before the shell starts, while `env:` delivers the value as a variable the script text never contains

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Expression substitution happens before bash runs, so the raw secret exists in the command string handed to the process, where `ps`, `set -x`, and error traces can surface it. An environment variable keeps the script text clean. Log masking applies either way, but masking is a log filter, not leak prevention.
</details>

---

### Question 4
**Which statement correctly distinguishes a cache from an artifact?**

- A) Artifacts are best-effort and may vanish; caches are guaranteed for 90 days
- B) Caches are keyed best-effort storage that speeds up later runs; artifacts carry outputs between jobs and to humans for a retention period
- C) They are interchangeable names for the same storage backend
- D) Caches are readable across branches while artifacts are run-local only

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A cache exists to avoid re-downloading or rebuilding and may be evicted under LRU pressure, so correctness must never depend on a hit. An artifact is the durable hand-off: uploaded by one job, downloadable by later jobs in the same run and from the run page for a configured retention window.
</details>

---

### Question 5
**With `strategy.fail-fast` left at its default, what happens when one matrix leg fails?**

- A) All legs run to completion and every result is reported
- B) The failing leg retries once, then the others continue
- C) The remaining legs are cancelled, hiding whether the failure was version-specific
- D) A new workflow run starts with only the failed combination

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `fail-fast` defaults to `true`, so the first red leg cancels its siblings. That saves runner minutes while destroying exactly the evidence you need when debugging, which is why `fail-fast: false` is the right setting while stabilizing a matrix.
</details>

---

### Question 6
**What does a top-level `concurrency` group with `cancel-in-progress: true` achieve on a busy branch?**

- A) Superseded runs are cancelled so only the newest commit's result matters
- B) Jobs inside a single run are forced to execute one at a time
- C) All workflows in the repository are serialized behind one lock
- D) Failed runs are retried automatically with fresh runners

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The group key allows one run per key; a newer queued run replaces the older pending one, and `cancel-in-progress` also kills the run currently executing. Five quick commits then produce one meaningful result instead of five full suites. Never enable cancellation for deploy or release runs.
</details>

---

### Question 7
**Which `uses:` reference is immutable?**

- A) `uses: actions/checkout@v4`
- B) `uses: actions/checkout@main`
- C) `uses: actions/checkout`
- D) `uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8`

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** A full 40-character commit SHA is content-addressed and cannot be moved. `@v4` is a mutable tag its maintainers can re-point, `@main` is a branch vulnerable to force-pushes, and a missing ref resolves to whatever the default branch currently is. Keep the human version in a trailing comment.
</details>

---

### Question 8
**Why can wiring `workflow_run` directly to untrusted output be dangerous?**

- A) It triggers an infinite loop of workflow runs
- B) The triggered workflow runs the default branch's file with a privileged token regardless of where the event originated, so conclusions and payloads must be validated
- C) It grants fork pull requests write access to the repository
- D) It bypasses branch-protection required checks

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `workflow_run` executes in the default-branch context with a normal privileged token, even when the workflow it watches processed untrusted input. That is why it is safe for trusted chaining — the example deploy pattern in `projects/06-devops/ci-cd/README.md` gates on `conclusion == 'success'` — and unsafe without payload validation when the upstream run was attacker-influenced.
</details>

---

### Question 9
**Why can `runs-on: ubuntu-latest` produce different results two weeks apart with no code change?**

- A) The label is randomly assigned to different data centers each run
- B) It always selects the newest nightly build of Ubuntu
- C) GitHub retargets the alias when it ships a new LTS image, changing preinstalled tool versions
- D) It cannot; the label only affects pricing, not the image

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `-latest` labels are moving aliases that GitHub repoints at new image generations, silently swapping preinstalled runtimes and build tools. Pinning the explicit label (for example `ubuntu-24.04`) trades automatic upgrades for reproducibility. This repository's `ci.yml` currently uses the mutable aliases on every job.
</details>

---

### Question 10
**What is GitHub's default maximum job duration before the platform terminates it?**

- A) 6 hours, which is why `timeout-minutes` should be set explicitly
- B) 60 minutes, for hosted runners only
- C) 24 hours, on every runner
- D) There is no limit; a hung job runs forever

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The six-hour ceiling means an unnoticed hang can burn hours of runner time — and six hours of wall-clock delay — before anything fails loudly. An explicit `timeout-minutes` turns a hang into a fast, diagnosable failure. None of the five jobs in this repo's `ci.yml` sets one yet.
</details>

---

### Question 11
**In this repository's real `ci.yml`, which pair of conditions fails the `docs` job?**

- A) A missing H1 heading, or a docs file longer than 500 lines
- B) Any spellcheck error, or a trailing-whitespace violation
- C) A failing pytest run, or a ruff error under `docs/`
- D) A relative `.md` link under `docs/` pointing at a file that does not exist, or a `**Last updated:**` stamp in `current-focus.md` older than 8 days

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** The job runs two gates: a broken-relative-link scan over every Markdown file under `docs/` (excluding `docs/plan/archive/`), which emits `::error file=...` annotations, and a freshness gate extracting the `**Last updated:**` stamp from `docs/tracking/current-focus.md` and failing when the age exceeds 8 days — or when no stamp exists at all.
</details>

---

### Question 12
**What do the `-Check` flags on `build-knowledge-index.ps1` and `build-skills-scoreboard.ps1` verify?**

- A) That the PowerShell scripts parse without syntax errors
- B) That the committed generated views (`docs/reference/INDEX.md`, `docs/roadmap/skills-scoreboard.md`) still match what the generators would produce from the registries
- C) That every registry entry references an existing documentation file
- D) That no knowledge-registry entry has been modified in the last 8 days

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** These files follow a generate, commit, verify pattern: authors regenerate locally and commit the output; CI re-runs the generator in check mode and fails when the committed file is stale against its source of truth — `registries/knowledge-registry.yaml` for the index and `registries/evidence.yaml` joined with the knowledge registry for the scoreboard. Hand-editing a generated view breaks the check.
</details>

---

### Question 13
**Which key is invalid in a job that calls a reusable workflow with `uses:` at the job level?**

- A) `needs:`
- B) `with:`
- C) `runs-on:`
- D) `secrets:`

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** A calling job is a reference, not a container: it may declare `uses`, `with`, `secrets`, `needs`, `if`, `strategy`, `permissions`, `concurrency`, and `environment`, but the runner and steps live inside the called workflow, so `runs-on:` and `steps:` belong to it, not to the caller.
</details>

---

### Question 14
**How does the `integration` job in `ci.yml` obtain Qdrant and Redis?**

- A) It declares them as `services:` containers on fixed ports, waits until the ports accept connections, then runs `pytest -m integration`
- B) It installs both databases with apt on the runner
- C) It authenticates to shared cloud instances using repository secrets
- D) It skips those tests in CI and runs them only on developer machines

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The job declares `qdrant/qdrant:v1.8.0` on port 6333 and `redis:7-alpine` on 6379 as `services:`, then a Python wait loop opens a socket to each port before `pytest -q -m integration` runs with `QDRANT_URL` and `REDIS_URL` pointed at `localhost`. The Qdrant version is pinned to match the client's supported API range.
</details>

---

### Question 15
**What does the legacy-lint step `ruff check . --statistics || true` mean?**

- A) Lint findings block the merge like any other gate
- B) The step retries once before failing the job
- C) Only statistics from the first file are checked
- D) The step always exits 0, so it is an advisory report; the job's real gate is `pytest -q`

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** `|| true` swallows the non-zero exit, so the step can never fail the job — it reports roughly 2.3k style findings across teaching files as information. The step name says "advisory" for exactly this reason, and the curriculum's test suite is the actual gate. A report and a gate must never be confused.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Medium | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Easy | | |
| 7 | Easy | | |
| 8 | Hard | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Hard | | |
| 13 | Hard | | |
| 14 | Medium | | |
| 15 | Easy | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | A | 6 | A | 11 | D |
| 2 | C | 7 | D | 12 | B |
| 3 | D | 8 | B | 13 | C |
| 4 | B | 9 | C | 14 | A |
| 5 | C | 10 | A | 15 | D |

---

*Generated for ai-engineer-lab - Quiz 01 of 01*
