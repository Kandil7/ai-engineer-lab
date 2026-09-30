# Session Operating Procedure

The five-step procedure for every learning session. Run this before,
during, and after the work.

---

## Step 1 — Define the Session (2 min)

Open a new session and fill in the goal card:

```markdown
## Session Goal
- **Topic/Feature:** [what you're learning/building]
- **What I already know:** [your starting point]
- **What I do not understand:** [the specific gap]
- **What I will write myself:** [the code you own]
- **What I want AI help with:** [the specific help]
```

**Rule:** If you can't fill this card, you're not ready to start. Narrow the scope.

---

## Step 2 — Start with the Smallest Useful Question (1 min)

**Bad:** "Build my auth service."
**Better:** "Explain JWT auth flow in a Go API."

**Bad:** "How does RAG work?"
**Better:** "How does chunk size affect retrieval quality?"

The question should be answerable in 5 minutes.

---

## Step 3 — Write Before Asking for the Answer (5-15 min)

Before asking AI anything, write:
- Pseudo-code or a sketch
- File structure
- Function signatures
- Request/response shapes
- What you think the answer is

**Why:** Writing first reveals what you actually know. Asking first
creates dependency.

---

## Step 4 — Capture Output as an Artifact (5 min)

Every AI session must leave a repo file. Pick one:

| Session type | Artifact | Location |
|-------------|----------|----------|
| Learned a concept | Learning walkthrough | `docs/learning/` |
| Built a feature | Plan + review | `projects/*/plan.md`, `ai-review.md` |
| Hit a bug | Debugging session | `debugging-session.md` |
| Made a mistake | Mistake record | `mistakes.md` |
| Read a source | Source summary | `docs/learning/source-summaries/` |
| Made a decision | ADR | `docs/decisions/` |

---

## Step 5 — Close the Loop (5 min)

Write a closing reflection:

```markdown
## Session Close
- **What changed:** [what was built/fixed/learned]
- **What I learned:** [the key insight]
- **What still feels weak:** [the remaining gap]
- **Next step:** [what to do next session]
```

---

## Session Checklist

- [ ] Session goal card filled in
- [ ] Smallest question identified
- [ ] Wrote my own attempt first
- [ ] Used the right agent for the situation
- [ ] Captured output as a repo artifact
- [ ] Wrote closing reflection
- [ ] Identified the next step

---

## Common Session Patterns

### Pattern: Learn a new concept
1. Learning Coach: "Explain [concept]"
2. Try to restate in your own words
3. Learning Coach: quiz me on [concept]
4. Record gaps in `mistakes.md`

### Pattern: Build a feature
1. Project Planner: plan [feature]
2. Write code manually (Phase C)
3. Pair Programmer: review my code (if needed)
4. Code Reviewer: review [feature]
5. Fix findings yourself
6. Write `ai-review.md`

### Pattern: Fix a bug
1. Collect evidence (error, expected, actual)
2. Debugging Specialist: hypotheses
3. Run diagnostics yourself
4. Confirm root cause
5. Fix manually
6. Write `debugging-session.md`

### Pattern: Study a source
1. Source Learning Agent: extract key ideas
2. Verify one claim yourself
3. Build the exercise
4. Map to the repo
5. Write `source-summary.md`
