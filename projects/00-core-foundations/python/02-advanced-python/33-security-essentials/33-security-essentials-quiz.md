# Advanced Python 33: Security Essentials — Quiz

> **Topic Overview**: Secrets, hashing, injection, deserialization, and prompt injection.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which module for security-sensitive randomness?**
- A) `random`
- B) `secrets`
- C) `math`
- D) `hashlib`

<details><summary>Reveal Answer</summary>**B.** Cryptographically secure.</details>

### Question 2 — Easy
**How should passwords be stored?**
- A) Plaintext
- B) Salted, slow hash (PBKDF2/bcrypt/argon2)
- C) MD5
- D) SHA1

<details><summary>Reveal Answer</summary>**B.** Slow, salted hashing.</details>

### Question 3 — Medium
**Why `hmac.compare_digest` instead of `==`?**
- A) It is faster
- B) Constant-time comparison avoids timing side channels
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Timing-safe equality.</details>

### Question 4 — Medium
**How do you prevent SQL injection?**
- A) Escape strings manually
- B) Parameterized queries, passing values separately from SQL
- C) Use regex
- D) Hash inputs

<details><summary>Reveal Answer</summary>**B.** Values never become SQL.</details>

### Question 5 — Medium
**Why avoid `shell=True`?**
- A) It is slower
- B) User input can be interpreted by the shell as commands
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Command injection.</details>

### Question 6 — Hard
**Why is `pickle` unsafe for untrusted data?**
- A) It is slow
- B) Unpickling can execute arbitrary code
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Deserialization is code execution.</details>

### Question 7 — Hard
**What does `yaml.safe_load` prevent?**
- A) Slow parsing
- B) Arbitrary object construction from YAML tags
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** No object instantiation.</details>

### Question 8 — Hard
**What is prompt injection?**
- A) SQL injection
- B) Instructions hidden in untrusted content that the model may follow
- C) A buffer overflow
- D) A cache bug

<details><summary>Reveal Answer</summary>**B.** Untrusted text as instructions.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You apply security essentials. |
| 5-6 | Review injection and deserialization. |
| < 5 | Re-read the lecture. |
