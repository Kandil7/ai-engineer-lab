# Reliability track built: 5 files in projects/06-devops/reliability

### Context

AI Engineer Lab, DevOps track. Task: author the reliability and distributed systems patterns lane (README, lecture, glossary, quiz, exercise) in the established Format B style, grounded only in verified repo facts, then run the five prescribed verifications.

### Explanation

Five files created under projects/06-devops/reliability/: README.md (123 lines), lectures/01-reliability-patterns-lecture.md (600), lectures/01-reliability-patterns-glossary.md (558, 47-term quick-reference table plus detailed definitions), quizzes/01-reliability-patterns-quiz.md (346, 15 questions), exercises/01-reliability-patterns.py (704). The exercise is a stdlib-only offline rule engine: 8 REL rules (REL001 no timeout through REL008 missing per-caller rate-limit key) run over policy packs. BAD pack trips all 8, GOOD pack raises zero, verified by demo run. Findings resolve real source lines by scanning the exercise file itself for marker comments of the form "# BAD:timeout" and "# GOOD:queue", one marker per rule trigger, resolved by _declared_line. JSON path argument accepts external policy files with the same rules: findings report line "-" and the process exits 1 on critical findings, 0 on clean, 2 on missing or invalid files. Components taught by working demo: Deadline, RetryPolicy (exponential backoff, full jitter, attempt cap, retryable-class predicate), CircuitBreaker (closed open half-open with failure-rate threshold, minimum samples, cooldown, single half-open trial), TokenBucketLimiter (one bucket per key), IdempotencyStore, FlakyDependency. All demos use seeded random.Random and a _FakeClock, so reruns are byte-identical (verified: two consecutive runs compare equal). Grounding facts used with paths: llm/client.py:146 and 157-162 and 214-219 and 773-775, index/embeddings.py:73 and 246 and 342, retrieve/retriever.py:56, index/vector_store.py:101 (gap: no timeout arg), api/main.py:65 and 146, infra/docker/docker-compose.yml:66-70 and 141-152, .github/workflows/ci.yml:71-77 and 140-154. Verified gaps stated as gaps: no circuit breaker, no DLQ, no SIGTERM handler anywhere in devmate/src, embedding cache without TTL or single-flight. Complement positioning recorded against registry nodes data.reliability and system-design.failure-modes.

### Alternatives

Line resolution options: AST parsing of the pack declarations (precise but heavy and fragile to dict formatting), placeholder line numbers computed by hand (drift on any edit), marker comments scanned in source text (chosen: zero dependencies, survives edits because the marker sits on the declaration line). JSON encoding: plain utf-8 rejected files saved with a Windows BOM, so switched to utf-8-sig which reads both. Glossary scope: 26 detailed definitions against roughly 44 planned terms; landed at 47 table terms plus 28 definitions, inside the 450-650 line target.

### Rationale (Why this?)

The current repo state will verify the file via python -m py_compile, a direct run, a byte-level CRLF scan of all five files, and the repo-structure and knowledge validators. A deliberately wrong pack makes the machine print the counter-example: the file states the answer key, and it is exercised as a runnable artifact.

### Next Steps

Verification results, all observed in this session: py_compile exit 0; demo exit 0 with BAD 4 critical 4 warning and GOOD 0; CRLF pairs 0 on all five files; repo-structure Passed 75 Failed 0 Warnings 0; knowledge Passed 11 Failed 0. Corrections made after first write: two lecture typos fixed (Dead-Lit-Danger, Dead-LLetter), README term count corrected 50 to 47 after counting the table, JSON loader switched to utf-8-sig after the BOM test failed. Zero rule changes were needed: no REL rule fired falsely on the GOOD pack. Unrelated pre-existing LSP error left untouched in projects/00-core-foundations path arabic-entity-resolution file (sys.stdout.reconfigure typed as TextIO). Follow-ups: decide whether to register the new files in any registry (registries validate with the files unregistered, so this was not required), and whether to commit (user decides).

---
