# MongoDB 05: Find — Quiz

> **Topic Overview**: Filters, projection, cursors, and `None` handling.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `find` return?**
- A) A list
- B) A cursor streaming from the server
- C) One document
- D) A count

<details><summary>Reveal Answer</summary>**B.** Lazy cursor.</details>

### Question 2 — Easy
**What does `find_one` return on no match?**
- A) `{}` 
- B) `None`
- C) An error
- D) An empty cursor

<details><summary>Reveal Answer</summary>**B.** `None` means miss.</details>

### Question 3 — Medium
**How do you exclude `_id` from projected output?**
- A) It is excluded by default
- B) `{"_id": 0}` explicitly
- C) You cannot
- D) `{"_id": None}`

<details><summary>Reveal Answer</summary>**B.** Explicit exclusion.</details>

### Question 4 — Medium
**Why is projection a secrecy control?**
- A) It is not
- B) Hashes and tokens must never leave the DB unless needed
- C) Speed only
- D) Style

<details><summary>Reveal Answer</summary>**B.** Least exposure.</details>

### Question 5 — Medium
**Why not `list()` an unbounded cursor?**
- A) Style
- B) It materializes everything and OOMs the client
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Bounded memory.</details>

### Question 6 — Hard
**What is `batch_size` for?**
- A) Speed only
- B) Bounding each network round-trip on large scans
- C) Limiting results
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Chunked streaming.</details>

### Question 7 — Hard
**Why do idle cursors die server-side?**
- A) A bug
- B) Timeout reclaims server resources; process steadily or manage explicitly
- C) They complete
- D) They lock

<details><summary>Reveal Answer</summary>**B.** Cursor timeouts.</details>

### Question 8 — Hard
**How should API code serialize a found document?**
- A) `json.dumps` directly
- B) With `bson.json_util` for `ObjectId`/dates
- C) `str(doc)`
- D) `repr`

<details><summary>Reveal Answer</summary>**B.** Type-safe serialization.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You read efficiently. |
| 5-6 | Review cursors and projection. |
| < 5 | Re-read the lecture. |
