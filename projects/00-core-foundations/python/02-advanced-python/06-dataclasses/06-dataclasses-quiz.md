# Advanced Python 06: Dataclasses — Quiz

> **Topic Overview**: Generated methods, `field`, frozen instances, and validation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `@dataclass` generate by default?**
- A) Only `__init__`
- B) `__init__`, `__repr__`, and `__eq__`
- C) `__hash__` always
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Boilerplate methods.</details>

### Question 2 — Easy
**What does `frozen=True` provide?**
- A) Caching
- B) Immutability and, with `eq=True`, a generated `__hash__`
- C) Slots only
- D) Validation

<details><summary>Reveal Answer</summary>**B.** Hashable and immutable.</details>

### Question 3 — Medium
**Why use `field(default_factory=list)`?**
- A) Style
- B) A plain mutable default would be shared across instances
- C) For speed
- D) For hashing

<details><summary>Reveal Answer</summary>**B.** Per-instance lists.</details>

### Question 4 — Medium
**When does `__post_init__` run?**
- A) Before `__init__`
- B) After the generated `__init__`, for validation or derived fields
- C) Never
- D) On hash

<details><summary>Reveal Answer</summary>**B.** Post-initialisation hook.</details>

### Question 5 — Medium
**Why can a dataclass with `eq=True` and mutable fields be unhashable?**
- A) It is always hashable
- B) Mutable state breaks the hash invariant, so `__hash__` is set to None
- C) Because of slots
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Equality without a stable hash is unsafe.</details>

### Question 6 — Hard
**What ordering must fields respect when some have defaults?**
- A) Any
- B) Fields without defaults must come before fields with defaults
- C) Alphabetical
- D) Type order

<details><summary>Reveal Answer</summary>**B.** Otherwise `__init__` is ambiguous.</details>

### Question 7 — Hard
**How does `slots=True` change a dataclass?**
- A) Nothing
- B) Generates `__slots__`, saving memory and preventing new attributes
- C) Enables hashing
- D) Adds validation

<details><summary>Reveal Answer</summary>**B.** Fewer bytes per instance.</details>

### Question 8 — Hard
**Why prefer dataclasses over hand-written classes for config/records?**
- A) Faster
- B) Less boilerplate, correct `repr`/`eq`, and easy immutability — fewer bugs
- C) They are required
- D) They support inheritance only

<details><summary>Reveal Answer</summary>**B.** Boilerplate is error-prone.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use dataclasses well. |
| 5-6 | Review `field`, `frozen`, `__post_init__`. |
| < 5 | Re-read the lecture. |
