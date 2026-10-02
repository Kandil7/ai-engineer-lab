# FastAPI 40: Authorization — Quiz

> **Topic Overview**: RBAC, ABAC, tenant isolation, and the confused deputy.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is authentication vs authorization?**
- A) Same thing
- B) Who you are vs what you may do
- C) Tokens vs sessions
- D) Login vs logout

<details><summary>Reveal Answer</summary>**B.** Identity vs permission.</details>

### Question 2 — Easy
**What is RBAC?**
- A) Row-level security
- B) Permissions attached to roles, roles attached to users
- C) Encryption
- D) Rate limiting

<details><summary>Reveal Answer</summary>**B.** Role-mediated access.</details>

### Question 3 — Medium
**When does ABAC beat RBAC?**
- A) Always
- B) When decisions need attributes (tenant, plan, ownership, time) roles cannot express
- C) Never
- D) For small apps

<details><summary>Reveal Answer</summary>**B.** Attribute-driven rules.</details>

### Question 4 — Medium
**Why check the resource, not just the role?**
- A) Style
- B) A role that may edit *some* records must not edit *all* of them
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Object-level checks.</details>

### Question 5 — Medium
**How do you isolate tenants?**
- A) One database each always
- B) A tenant key on every query plus enforced context from the authenticated identity
- C) Trust the client
- D) Rate limit

<details><summary>Reveal Answer</summary>**B.** Tenant-scoped access.</details>

### Question 6 — Hard
**What is the confused-deputy problem?**
- A) A slow server
- B) A privileged service acting on attacker-supplied identifiers without checking it may
- C) A cache bug
- D) A slow query

<details><summary>Reveal Answer</summary>**B.** Authority vs intent mismatch.</details>

### Question 7 — Hard
**Why enforce permissions in dependencies rather than in handlers?**
- A) Style
- B) Refactoring a handler cannot accidentally drop the check
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Checks travel with the route.</details>

### Question 8 — Hard
**Why deny by default?**
- A) Slower
- B) Forgotten rules fail closed instead of leaking
- C) Caching
- D) Style

<details><summary>Reveal Answer</summary>**B.** Closed by default.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You authorize safely. |
| 5-6 | Review RBAC/ABAC and tenant checks. |
| < 5 | Re-read the lecture. |
