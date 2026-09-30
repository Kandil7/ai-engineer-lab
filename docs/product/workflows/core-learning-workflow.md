# Core Learning Workflow (Phases A-G)

> **Superseded.** The canonical, validator-gated workflow chain is
> [`.ai/workflows/feature/`](../../../.ai/workflows/feature/01-plan.md)
> (`01-plan` through `06-reflect`). Edit `.ai/` and not this file; this copy is kept
> as product-era documentation.

The seven-phase workflow for every learning session. Each phase has a
purpose, a duration, and a deliverable.

---

## Phase A — Understand First (5-10 min)

**Purpose:** Build the mental model before touching code.

**Ask yourself:**
1. What concept is this built on?
2. What are the 2-3 key ideas?
3. What is the smallest working example?
4. What do I already know vs not know?

**Use:** Learning Coach agent.

**Deliverable:** A 3-sentence statement of the concept in your own words.

```markdown
## Concept: [name]
- What it is: [one sentence]
- Why it matters: [one sentence]
- Key idea: [the one thing to remember]
```

---

## Phase B — Plan Before Code (5-10 min)

**Purpose:** Define what "done" looks like before writing.

**Use:** Project Planner agent.

**Deliverable:** A small feature plan.

```markdown
## Plan: [feature]
- Goal: [what we're building]
- Files: [what to create/change]
- Input/output: [data shapes]
- Dependencies: [what must exist first]
- MVP boundary: [in/out]
- First test: [how to verify it works]
```

---

## Phase C — Write Code Manually (20-35 min)

**Purpose:** The learner writes the core logic. This is the work.

**You write:**
- Function signatures
- Control flow
- Main logic and conditionals
- Validation
- Branch conditions
- Integration logic

**AI may help with:**
- Boilerplate
- Naming suggestions
- Syntax reminders
- Framework setup

**Rule:** If you can't explain a line you wrote, delete it and rewrite.

---

## Phase D — Ask for Hints, Not Rescue (5-10 min)

**Purpose:** Get unblocked without getting the answer.

**When blocked:**
1. State exactly what you understand.
2. State exactly where you're stuck.
3. Ask for "the next step" or "the smallest hint."

**Never ask:** "Write the whole answer."

**Escalation:**
| Attempt | Ask for |
|---------|---------|
| 1st | Conceptual hint |
| 2nd | API/pattern hint |
| 3rd | Pseudocode hint |
| Rescue | 3-5 lines (then rewrite from memory) |

**Use:** Pair Programmer agent.

---

## Phase E — Review After Implementation (5-10 min)

**Purpose:** Catch bugs and design issues before they compound.

**Use:** Code Reviewer agent.

**Deliverable:** `ai-review.md` with findings.

**Process:**
1. Show the reviewer your code.
2. Get findings with severity.
3. Fix issues yourself (don't let AI rewrite).
4. Re-run if critical issues found.

---

## Phase F — Debug with Evidence (5-10 min)

**Purpose:** Diagnose failures systematically.

**Before asking AI, collect:**
1. Error output (full traceback)
2. Expected behavior
3. Actual behavior
4. Relevant files
5. Recent changes

**Use:** Debugging Specialist agent.

**Deliverable:** `debugging-session.md` or `mistakes.md` entry.

---

## Phase G — Reflect and Retain (5-10 min)

**Purpose:** Convert experience into long-term learning.

**Write:**
1. What was built (1-2 sentences)
2. What you misunderstood (the gap)
3. What the reviewer found (the lesson)
4. What to remember (the takeaway)

**Deliverable:** One of:
- `docs/learning/` walkthrough
- `mistakes.md` entry
- `notes.md` update
- ADR (if a decision was made)

---

## Phase Summary

| Phase | Duration | Output | Agent |
|-------|----------|--------|-------|
| A — Understand | 5-10 min | Concept statement | Learning Coach |
| B — Plan | 5-10 min | Feature plan | Project Planner |
| C — Write | 20-35 min | Working code | (you) |
| D — Hints | 5-10 min | Unblocked | Pair Programmer |
| E — Review | 5-10 min | `ai-review.md` | Code Reviewer |
| F — Debug | 5-10 min | `debugging-session.md` | Debugging Specialist |
| G — Reflect | 5-10 min | Learning artifact | Learning Coach |

**Total:** 50-90 minutes per session.
