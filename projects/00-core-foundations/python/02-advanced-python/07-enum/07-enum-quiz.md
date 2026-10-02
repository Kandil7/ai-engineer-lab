# Advanced Python 07: Enums — Quiz

> **Topic Overview**: Named constants, `auto`, custom methods, and state machines.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why use an `Enum` instead of string constants?**
- A) Speed
- B) A fixed, named set of members that cannot be typo'd or silently extended
- C) Memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Closed, validated set.</details>

### Question 2 — Easy
**What does `auto()` do?**
- A) Hides members
- B) Assigns automatic, distinct values to members
- C) Sorts
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Auto numbering.</details>

### Question 3 — Medium
**What does `IntEnum` add over `Enum`?**
- A) Nothing
- B) Members are also `int`, so comparisons and numeric use work
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Subclass of int.</details>

### Question 4 — Medium
**How do you look up a member by value?**
- A) `Enum.member`
- B) `Enum(value)`
- C) `getattr`
- D) Index

<details><summary>Reveal Answer</summary>**B.** Value constructor.</details>

### Question 5 — Medium
**Why are enums useful in state machines?**
- A) Speed
- B) States are a closed set; transitions can be validated against allowed pairs
- C) Memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Explicit states prevent invalid ones.</details>

### Question 6 — Hard
**Can an enum member's value be changed after definition?**
- A) Yes
- B) No; members are created once at class definition and are effectively immutable
- C) Only with auto
- D) Only in IntEnum

<details><summary>Reveal Answer</summary>**B.** Closed at definition.</details>

### Question 7 — Hard
**What happens if two members share the same value?**
- A) Error
- B) The second becomes an alias of the first (same member)
- C) They merge names
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Aliasing is explicit via `@unique` to prevent.</details>

### Question 8 — Hard
**Why combine enums with dataclasses?**
- A) For speed
- B) The dataclass field gets a typed, closed value rather than a loose string
- C) For hashing
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Strong typing for state fields.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand enums. |
| 5-6 | Review IntEnum, lookup, and aliases. |
| < 5 | Re-read the lecture. |
