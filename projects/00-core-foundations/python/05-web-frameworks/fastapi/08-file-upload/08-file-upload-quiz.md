# FastAPI 08: File Upload — Quiz

> **Topic Overview**: `UploadFile`, streaming, and size limits.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you accept a file upload?**
- A) `file: UploadFile = File(...)`
- B) `file: str`
- C) `file: Body(...)`
- D) `file: Query(...)`

<details><summary>Reveal Answer</summary>**A.** `UploadFile` plus `File`.</details>

### Question 2 — Easy
**What does `UploadFile` expose?**
- A) The path
- B) `.filename`, `.content_type`, and an async `.read()`
- C) The database id
- D) The user

<details><summary>Reveal Answer</summary>**B.** Metadata and async reading.</details>

### Question 3 — Medium
**Why stream a large upload rather than `await file.read()` all at once?**
- A) For speed only
- B) Reading all of it loads the whole file into memory
- C) It is required
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Bounded memory.</details>

### Question 4 — Medium
**How do you enforce a maximum upload size?**
- A) You cannot
- B) Check the size while streaming and abort, or cap at the server/proxy
- C) By extension
- D) By MIME only

<details><summary>Reveal Answer</summary>**B.** Explicit size cap.</details>

### Question 5 — Medium
**Why validate content type and not only the extension?**
- A) Style
- B) Extensions are attacker-controlled; sniff or validate the actual type
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Trust content, not names.</details>

### Question 6 — Hard
**What is the risk of writing an upload to a path derived from its filename?**
- A) None
- B) Path traversal (`../../`) can escape the intended directory
- C) It is slower
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Sanitize/generate filenames.</details>

### Question 7 — Hard
**Why is a file upload a resource-exhaustion surface?**
- A) It is not
- B) Unbounded uploads and concurrent large streams can exhaust memory/disk
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Cap size and concurrency.</details>

### Question 8 — Hard
**Where should virus/malware scanning sit?**
- A) In the request handler synchronously
- B) Off the request path, after upload, before the file is used
- C) Never
- D) On the client

<details><summary>Reveal Answer</summary>**B.** Async scan.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle uploads safely. |
| 5-6 | Review streaming and size caps. |
| < 5 | Re-read the lecture. |
