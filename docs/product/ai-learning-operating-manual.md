# AI Learning Operating Manual

> **Long-track context.** Written 2026-08-06, before the 10-week active track. The plan
> of record is [`active-track-10-week.md`](../roadmap/active-track-10-week.md); treat
> roadmap-specific claims here as historical (the AI usage principles themselves remain valid).

**Last updated:** 2026-08-06

How to use AI agents inside `ai-engineer-lab` to accelerate learning **without** outsourcing understanding.

> **You are the driver.** AI explains, plans, reviews, and debugs. You write the core logic.

---

## Principles

### 1. The learner owns the logic
AI can explain, guide, review, and debug. You write the main logic, conditionals, flow, and core implementation by hand.

### 2. AI is a tutor, planner, reviewer, and debugger first
```
Understand → Plan → Write manually → Hint if blocked → Review → Debug with evidence → Record
```

### 3. Every AI interaction creates an artifact
Each meaningful AI session ends in at least one repo file: `plan.md`, `ai-review.md`, `mistakes.md`, `debugging-session.md`, `source-summary.md`.

### 4. Small slices beat giant prompts
One concept, one feature, one bug, one review — not "build my entire project."

### 5. Prompts are engineering assets
Versioned, named, scoped, reviewed, improved over time.

---

## Agent Roles

### Learning Coach
**Purpose:** Teach concepts, probe understanding, give exercises, identify weaknesses.

**Use when:** Starting a new topic, stuck conceptually, wanting active recall questions.

**Prompt:**
```text
You are my AI Engineering mentor.
Your goal is to help me learn, not replace my thinking.

Rules:
- Explain simply first.
- Give one practical example.
- Then give me a small challenge.
- Do not give the full solution unless I explicitly ask.
- Review my attempt before showing the answer.
- Identify my conceptual weaknesses.
- Use Socratic questioning when possible.
```

### Project Planner
**Purpose:** Convert features into files, tasks, execution order, MVP boundaries.

**Use when:** Starting a new feature, scoping a service, breaking large tasks.

**Prompt:**
```text
You are a Project Planner for a learning-by-building repository.

Your job:
1. Break the feature into small tasks.
2. Identify files that should be created or changed.
3. Define the MVP boundary.
4. Suggest implementation order.
5. Suggest the first validation step.

Rules:
- Keep the plan concrete.
- Prefer the smallest viable slice.
- Do not write the full implementation code.
```

### Pair Programmer
**Purpose:** Support implementation in small guided steps while keeping you in control.

**Use when:** You know what to build but need help with the next step.

**Prompt:**
```text
You are my senior pair programmer.

Rules:
- Do not write the whole feature at once.
- Break implementation into small steps.
- Give me only the next step unless I ask for more.
- Assume I will write the code myself.
- If I get stuck, give hints first.
- Review my code before proposing a rewrite.
```

### Code Reviewer
**Purpose:** Critique code quality after you've written it.

**Use when:** A feature compiles or mostly works, you want structured feedback.

**Prompt:**
```text
You are a staff engineer reviewing my code.

Review for:
- readability
- maintainability
- correctness
- security
- performance

Output:
1. Findings
2. Severity
3. Why it matters
4. Minimal fix direction

Do not rewrite the full code unless requested.
```

### Debugging Specialist
**Purpose:** Diagnose failures systematically.

**Use when:** Runtime errors, wrong behavior, failing tests.

**Prompt:**
```text
You are an expert debugging engineer.

Process:
1. Analyze symptoms.
2. Generate hypotheses.
3. Rank likelihood.
4. Suggest diagnostics.
5. Wait for evidence before concluding.

Do not jump to the final answer immediately.
```

### Source Learning Agent
**Purpose:** Turn docs, repos, notebooks, articles into structured learning artifacts.

**Use when:** Reading official docs, studying a reference repo, going through a tutorial.

**Prompt:**
```text
You are a source-learning agent.

Given a doc, repo, notebook, article, or course module:
1. Extract the key ideas.
2. Separate confirmed facts from inferred conclusions.
3. Explain why the source matters.
4. Suggest one practical exercise.
5. Map it to the relevant folder in ai-engineer-lab.

Do not produce generic summaries.
```

---

## The Four-Level Help Model

The safest way to use AI without harming learning quality.

| Level | When | Ask For |
|-------|------|---------|
| **1. Explain** | Don't understand the topic | Simple explanation, intuition, analogy, tiny example |
| **2. Hint** | Mostly understand but blocked | Next step only, smallest hint, conceptual mistake |
| **3. Review** | Already attempted the work | Review my code/explanation, identify weaknesses |
| **4. Rescue** | After serious effort | Minimal working example, line-by-line explanation |

**After rescue:** Rewrite the logic manually from memory.

---

## Core Learning Workflow

### Phase A — Understand first
Before coding, ask: What concept is this built on? What are the 2-3 key ideas? What's the smallest working example?

### Phase B — Plan before code
Create a small feature plan: goal, files, input/output, dependencies, MVP boundary, first test.

### Phase C — Write the code manually
You write: function signatures, control flow, main logic, validation, branch conditions, integration logic.
AI may assist with: boilerplate, naming, syntax reminders, framework setup.

### Phase D — Ask for hints, not rescue
If blocked: "What should I do next?" → not "Write the whole answer."

### Phase E — Review after implementation
Run Code Reviewer after each feature slice. Store in `ai-review.md`. Fix issues yourself.

### Phase F — Debug with evidence
Collect: error output, logs, expected behavior, actual behavior, relevant files. Then use Debugging Specialist.

### Phase G — Reflect and retain
Write: what was built, what you misunderstood, what the reviewer found, what to remember.

---

## Where Each Agent Fits in the Repo

| Agent | Primary folders |
|-------|----------------|
| Learning Coach | `docs/learning/`, `docs/reviews/`, `projects/*/notes.md` |
| Project Planner | `projects/*/plan.md`, `docs/product/`, `docs/roadmap/` |
| Pair Programmer | active project folder under `projects/` |
| Code Reviewer | `ai-review.md`, `templates/code-review.template.md` |
| Debugging Specialist | `debugging-session.md`, `mistakes.md` |
| System Architect | `docs/architecture/`, `docs/decisions/`, `architecture-review.md` |
| Source Learning Agent | `learning-sources/`, `docs/learning/source-summaries/` |

---

## Usage by Project Area

### `00-core-foundations/`
AI as tutor + quiz generator. Study topic → ask 3 questions → solve by hand → get feedback → record.

### `03-databases/`
AI to explain normalization/indexing, review schema proposals, analyze queries.
Write manually: schema drafts, sample queries, migration structure.

### `04-ai-engineering/`
AI to explain embeddings/chunking/retrieval, convert docs to notes, plan RAG pipeline, review failures.
Write manually: pipeline notes, experiment definitions, evaluation criteria, integration logic.

### `05-system-design/`
You sketch first, then ask architect to critique. Revise. Write ADR if decision matters.

### `06-devops/`
AI to explain Docker, plan infra, debug environment, review deployment.
Write manually: Dockerfiles, compose adjustments, deployment runbooks.

---

## Session Operating Procedure

### Step 1 — Define the session
```md
## Session Goal
- Topic/Feature:
- What I already know:
- What I do not understand:
- What I will write myself:
- What I want AI help with:
```

### Step 2 — Start with the smallest useful question
Bad: "Build my RAG system."
Better: "Explain how hybrid retrieval fuses dense + BM25 results."

### Step 3 — Write before asking for the answer
Write pseudo-code, file structure, sketch request/response, write function signature.

### Step 4 — Capture output as an artifact
Save to `plan.md`, `ai-review.md`, `source-summary.md`, etc.

### Step 5 — Close the loop
Write: what changed, what you learned, what still feels weak, next step.

---

## What to Ask AI For vs What to Do Yourself

| Task | AI helps with | You do manually |
|------|--------------|-----------------|
| Understand a concept | Explanation + examples | Restate from memory |
| Break feature into steps | Yes | Approve and adjust |
| Write all core logic | **No** | Yes |
| Generate boilerplate | Sometimes | Review and integrate |
| Review code quality | Yes | Apply fixes manually |
| Diagnose bugs | With evidence | Run diagnostics and verify |
| Create learning notes | Draft structure | Finalize in your own words |
| Make architecture decisions | Discuss and critique | Own the final decision |

---

## Anti-Dependency Rules

1. **Never** ask for a full project implementation as the default.
2. **Never** merge AI-generated code you do not understand.
3. **Never** skip writing your own first attempt for core logic.
4. **Never** use AI review as a substitute for testing.
5. **Never** store raw AI output without refining it into a repo artifact.
6. **Never** let AI-generated design bypass an ADR for long-lived decisions.

---

## Daily 90-Minute Session

| Time | Activity |
|------|----------|
| 10 min | Choose topic/feature, define goal |
| 15 min | Learn/explain with Learning Coach |
| 35 min | Write code manually |
| 10 min | Ask Pair Programmer for one blocked step if needed |
| 10 min | Run review or debugging |
| 10 min | Write artifact and reflection |

**Daily minimum:** code change OR review note OR debugging note OR learning summary OR ADR draft.

---

## Success Criteria

This model is working if:
- You write more core logic yourself over time
- AI sessions become shorter and more precise
- Review findings become less repetitive
- Debugging becomes hypothesis-driven
- Repository contains growing reusable learning artifacts
- You can explain code after writing it

---

## Final Rule

> **Use AI to make learning faster, clearer, and more structured.**
> **Do not use AI to escape the struggle that produces real engineering skill.**
