# Advanced Python 11: collections — Quiz

> **Topic Overview**: `Counter`, `defaultdict`, `deque`, `namedtuple`, and `OrderedDict`.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `Counter` return for `most_common(3)`?**
- A) Sorted keys
- B) The three most frequent items with counts
- C) Unique items
- D) A dict

<details><summary>Reveal Answer</summary>**B.** Frequency ranking.</details>

### Question 2 — Easy
**What does `defaultdict(list)` do on a missing key?**
- A) Raises KeyError
- B) Inserts a new `list()` and returns it
- C) Returns None
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Default factory.</details>

### Question 3 — Medium
**Why use `deque` over a list for a queue?**
- A) Sorting
- B) O(1) `append`/`popleft` at both ends
- C) Hashing
- D) Memory

<details><summary>Reveal Answer</summary>**B.** Fast both-end operations.</details>

### Question 4 — Medium
**What does `maxlen` on a `deque` do?**
- A) Locks
- B) Drops the oldest items when full, giving a fixed-size buffer
- C) Sorts
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Bounded ring buffer.</details>

### Question 5 — Medium
**What does `namedtuple` give over a tuple?**
- A) Mutability
- B) Named field access plus tuple behavior
- C) Hashing only
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Readable, immutable records.</details>

### Question 6 — Hard
**When is `OrderedDict` still needed in modern Python?**
- A) Always
- B) For order-sensitive operations like `move_to_end`/`popitem(last=False)`; plain dicts keep insertion order
- C) Never
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Extra ordered methods.</details>

### Question 7 — Hard
**What subtle bug can `defaultdict` cause?**
- A) None
- B) Reading a missing key mutates the dict, so membership changes as a side effect
- C) It sorts
- D) It is slower

<details><summary>Reveal Answer</summary>**B.** Use `get` to avoid accidental inserts.</details>

### Question 8 — Hard
**Why is `Counter` arithmetic useful?**
- A) It is not
- B) Counters support `+`/`-`/`&`/`|`, enabling multiset operations
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Multiset algebra.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use collections well. |
| 5-6 | Review defaultdict and deque. |
| < 5 | Re-read the lecture. |
