# FastAPI 27: API Versioning — Quiz

> **Topic Overview**: Breaking vs additive changes and versioning styles.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When is a new version required?**
- A) Every change
- B) On breaking changes (removing/renaming fields, changing types/meaning)
- C) Never
- D) On bug fixes

<details><summary>Reveal Answer</summary>**B.** Breaking changes only.</details>

### Question 2 — Easy
**Give an additive change.**
- A) Removing a field
- B) Adding an optional field
- C) Renaming a field
- D) Changing a status code

<details><summary>Reveal Answer</summary>**B.** Backward compatible.</details>

### Question 3 — Medium
**Which versioning style is most cache-friendly?**
- A) Header
- B) URL path (`/v1/...`)
- C) Media type
- D) Query

<details><summary>Reveal Answer</summary>**B.** Explicit and cacheable.</details>

### Question 4 — Medium
**Why are header/media-type versioning harder to use in a browser?**
- A) They are not
- B) You cannot paste a versioned header into the address bar; URL versioning is linkable
- C) For speed
- D) They cache

<details><summary>Reveal Answer</summary>**B.** Discoverability.</details>

### Question 5 — Medium
**What supports a transition window?**
- A) Immediate removal
- B) Running v1 and v2 side by side until clients migrate
- C) Breaking old clients
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Coexistence.</details>

### Question 6 — Hard
**Why communicate deprecation with headers?**
- A) Style
- B) `Deprecation`/`Sunset` headers give clients a machine-readable timeline
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Predictable migration.</details>

### Question 7 — Hard
**What is the cost of never versioning?**
- A) None
- B) You can never make a breaking change without breaking clients, so the API ossifies
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Frozen evolution.</details>

### Question 8 — Hard
**What is the trap of versioning too eagerly?**
- A) None
- B) Fragmenting the surface and multiplying maintenance for changes that were actually compatible
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Prefer additive.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You version APIs correctly. |
| 5-6 | Review breaking vs additive and styles. |
| < 5 | Re-read the lecture. |
