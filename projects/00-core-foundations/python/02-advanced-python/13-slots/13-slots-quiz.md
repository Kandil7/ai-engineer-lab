# Advanced Python 13: `__slots__` — Quiz

> **Topic Overview**: Fixed attribute sets, memory savings, and their tradeoffs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `__slots__` do?**
- A) Locks attributes
- B) Reserves a fixed set of attributes, removing the per-instance `__dict__`
- C) Caches
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** No instance dict.</details>

### Question 2 — Easy
**What is the main benefit?**
- A) Speed only
- B) Lower memory per instance for many objects
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Fewer bytes each.</details>

### Question 3 — Medium
**What happens when you assign an attribute not in `__slots__`?**
- A) It is added dynamically
- B) `AttributeError`, because there is no `__dict__`
- C) It is ignored
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Closed attribute set.</details>

### Question 4 — Medium
**What must a subclass define to keep slotted behavior?**
- A) Nothing
- B) Its own `__slots__`, or it reintroduces `__dict__`
- C) A property
- D) A metaclass

<details><summary>Reveal Answer</summary>**B.** Otherwise memory savings are lost.</details>

### Question 5 — Medium
**How does `__slots__` interact with `@property`?**
- A) Conflict
- B) You can define a property, but the backing storage needs a different slot name
- C) They are identical
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Avoid name collisions.</details>

### Question 6 — Hard
**Why might `functools.cached_property` fail on a slotted class?**
- A) It works everywhere
- B) It needs a `__dict__` to store the cached value unless you add `__dict__` to slots
- C) It is faster
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Cache storage needs a dict slot.</details>

### Question 7 — Hard
**When is `__slots__` not worth it?**
- A) Never
- B) When few instances exist or dynamic attributes are needed
- C) For many instances
- D) For dataclasses

<details><summary>Reveal Answer</summary>**B.** Optimise with evidence.</details>

### Question 8 — Hard
**What does `dataclass(slots=True)` do?**
- A) Breaks the class
- B) Generates `__slots__` for the fields automatically
- C) Adds validation
- D) Enables hashing

<details><summary>Reveal Answer</summary>**B.** Convenient slotted records.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand `__slots__`. |
| 5-6 | Review inheritance and property interaction. |
| < 5 | Re-read the lecture. |
