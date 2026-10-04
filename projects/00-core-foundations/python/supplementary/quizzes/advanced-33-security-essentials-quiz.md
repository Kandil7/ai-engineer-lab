# Advanced Python Quiz 33 — Security Essentials

**Course:** AI Engineer — Core Foundations · Python
**Level:** Advanced · **Topic:** 33 — Security Essentials
**Questions:** 20 (6 Easy · 9 Medium · 5 Hard)
**Time:** 30 minutes

---

## Instructions

- Each question has exactly **one** correct answer (A–D).
- **Code-output questions** show code; choose the output.
- Answers and explanations are at the end — do the quiz **before** reading the key.
- Score yourself: `Score Tracking` section at the end.

---

## Questions

### Easy

**1. Which module must generate security tokens (API keys, OTPs)?**

A) `random`
B) `secrets`
C) `math`
D) `string`

**2. Which hash family is acceptable for storing passwords?**

A) MD5
B) SHA1
C) PBKDF2 (or bcrypt/argon2)
D) Plain SHA256 with no salt

**3. What does `hmac.compare_digest` provide that `==` does not?**

A) Faster comparison
B) Constant-time comparison, resistant to timing attacks
C) Automatic hashing
D) Case-insensitive matching

**4. What does `shell=True` in `subprocess.run` enable?**

A) Faster execution
B) Command injection via input metacharacters
C) Automatic argument escaping
D) Windows-only behavior

**5. What does `yaml.safe_load` refuse that `yaml.load` accepts?**

A) Multi-line strings
B) Python-object tags like `!!python/object/apply:...`
C) Nested mappings
D) Numeric values

**6. Why must API keys never appear in logs?**

A) Logs are slow
B) Logs are searched by attackers and ingested by monitoring
C) Logs are deleted daily
D) Keys expire faster in logs

### Medium

**7. Given:**

```python
import random

random.seed(42)
a = "".join(random.choice("abcd") for _ in range(4))
random.seed(42)
b = "".join(random.choice("abcd") for _ in range(4))
print(a == b)
```

**What is the output?**

A) `False` — random is unpredictable
B) `True` — same seed reproduces the same sequence
C) `False` — seeds only affect integers
D) Error — `choice` requires a list

**8. Two users choose the same password. Why do their stored hashes differ?**

A) The hash function is random
B) Each hash uses a fresh random salt
C) The database adds a secret key
D) They do not differ in secure systems

**9. `verify_password` returns `hmac.compare_digest(candidate, digest)`. Why is `candidate == digest` wrong?**

A) `==` compares objects, not bytes
B) `==` exits early on mismatch, leaking timing information
C) `==` is slower for short inputs
D) `==` cannot compare bytes

**10. Given the injection payload `1' OR '1'='1` against a parameterized query `WHERE id = ?`: what happens?**

A) All rows are returned
B) An empty list is returned — the payload is treated as a literal value
C) The query crashes
D) The table is dropped

**11. Why does `resolve()` matter before `is_relative_to(root)`?**

A) `resolve()` makes paths lowercase
B) `resolve()` collapses `..` and symlinks into the real absolute path
C) `resolve()` checks file existence
D) `resolve()` converts to relative paths

**12. What does `pickle.loads` do with a payload whose `__reduce__` returns `(os.system, ("echo PWNED",))`?**

A) Raises `ValueError` — pickle cannot serialize `os`
B) Stores the tuple without executing it
C) Executes `os.system("echo PWNED")` — deserialization is code execution
D) Returns a copy of the string

**13. What is ReDoS?**

A) A virus spread through regex libraries
B) Exponential regex backtracking on crafted input — CPU exhaustion
C) A memory leak in `re` module
D) A database denial-of-service

**14. What is the correct SQL query pattern?**

A) `f"SELECT name FROM users WHERE id = '{uid}'"`
B) `"SELECT name FROM users WHERE id = %s" % uid`
C) `"SELECT name FROM users WHERE id = ?", (uid,)`
D) `"SELECT name FROM users WHERE id = " + uid`

**15. Why is `verify=False` in an HTTP client dangerous?**

A) It disables TLS encryption entirely
B) It disables certificate verification — the peer is unauthenticated
C) It makes requests slower
D) It only affects HTTP/2

### Hard

**16. Which statement correctly characterizes prompt injection?**

A) It is a Python syntax error
B) It is the LLM-era injection class: untrusted text in a prompt becomes instructions, mirroring SQL injection
C) It only affects chat models, never RAG systems
D) It is prevented by longer prompts

**17. An agent resolves the LLM's tool choice. Which is safe?**

A) `eval(model_says)`
B) `TOOLS[model_says]` — a dispatch table of registered callables
C) `exec("call_" + model_says)`
D) `getattr(sys.modules["__main__"], model_says)()`

**18. Given:**

```python
class Evil:
    def __reduce__(self):
        return (os.system, ("echo PWNED",))


payload = pickle.dumps(Evil())
pickle.loads(payload)
```

**What is the output?**

A) `PWNED` printed — then the process continues
B) `AttributeError`
C) Nothing — `__reduce__` is ignored on load
D) `TypeError: os.system is not picklable`

**19. Which combination correctly hardens a batch job that embeds user-uploaded documents?**

A) `pickle.loads` on uploads + `yaml.load` for config + `shell=True` for preprocessing
B) Parameterized storage + `resolve()`-checked paths + `secrets` for API keys + `safe_load` config + least-privilege worker
C) `eval` for filters + unsalted MD5 for tokens + logs with full keys
D) Whitelisted `random.seed(time.time())` tokens + `verify=False`

**20. A config YAML contains `model: !!python/object/apply:os.system ['echo x']`. With `yaml.safe_load`:**

A) The config loads and runs `echo x`
B) `yaml.YAMLError` is raised — the tag is refused
C) The tag is silently ignored
D) A `KeyError` is raised

---

## Score Tracking

| Section | Count | Your Score |
|---------|-------|------------|
| Easy (Q1–6) | 6 | /6 |
| Medium (Q7–15) | 9 | /9 |
| Hard (Q16–20) | 5 | /5 |
| **Total** | **20** | **/20** |

**Rating:** 18–20 → Security-hygiene ready · 14–17 → Review sections 4.1–4.8 · <14 → Re-read the lecture, especially injection classes and deserialization.

---

## Answer Key

**1. B** — `secrets` uses the OS CSPRNG; `random` is a seeded PRNG.
*Distractors:* A is predictable, C is math, D is constants.

**2. C** — PBKDF2/bcrypt/argon2 are slow, salted KDFs; MD5/SHA1 and unsalted SHA256 are brute-forceable.
*Distractors:* A/B instant brute force, D lacks salt and KDF slowness.

**3. B** — `compare_digest` runs in constant time; `==` exits at the first mismatch.
*Distractors:* A false, C/D unrelated.

**4. B** — `shell=True` pipes input through a shell where `;` and backticks become commands.
*Distractors:* A false, C is the opposite, D false (dangerous everywhere).

**5. B** — `safe_load` refuses Python-object tags (`!!python/object/apply:...`).
*Distractors:* A/C/D are plain YAML features `safe_load` supports.

**6. B** — Logs are searched by attackers and ingested by monitoring tools; a logged key is a leaked key.
*Distractors:* A/C false, D is not the reason.

**7. B** — `random.seed(42)` reproduces the identical sequence — that is why it is predictable.
*Distractors:* A is the intuition that fails, C false, D false.

**8. B** — Each hash uses a fresh random salt, so identical passwords hash differently.
*Distractors:* A (not random — deterministic given salt), C (not the mechanism), D false.

**9. B** — `==` leaks prefix-match timing; `compare_digest` hides it.
*Distractors:* A (both are bytes), C false, D false.

**10. B** — With placeholders the payload is a literal value; no row matches.
*Distractors:* A is the *unsafe* outcome, C/D false.

**11. B** — `resolve()` normalizes `..` and symlinks to the real path; containment is then meaningful.
*Distractors:* A/C/D wrong about what resolve does.

**12. C** — Unpickling invokes the `(callable, args)` from `__reduce__` — RCE.
*Distractors:* A false, B false, D false.

**13. B** — Nested quantifiers backtrack exponentially on near-misses; one request can burn minutes of CPU.
*Distractors:* A/C/D are wrong categories.

**14. C** — Placeholder binding keeps input as data.
*Distractors:* A interpolation, B string formatting (same flaw), D concatenation (same flaw).

**15. B** — `verify=False` skips certificate checks; encryption remains but the peer is unauthenticated (MITM).
*Distractors:* A false (still encrypted), C false, D false.

**16. B** — Untrusted text (documents, web content) concatenated into prompts becomes instructions — the LLM-era injection class.
*Distractors:* A wrong category, C false (RAG is a prime target), D false.

**17. B** — A dispatch table limits the model to registered callables.
*Distractors:* A/C/D execute model-chosen code — RCE via model output.

**18. A** — Unpickling runs `os.system("echo PWNED")`; the process continues.
*Distractors:* B/C/D all misunderstand pickle's execution semantics.

**19. B** — Parameterized storage, contained paths, CSPRNG secrets, `safe_load`, least privilege.
*Distractors:* A/C/D each contain an RCE or secret-leak flaw.

**20. B** — `safe_load` refuses Python-object tags and raises `yaml.YAMLError`.
*Distractors:* A is `yaml.load` behavior, C false, D wrong exception.
