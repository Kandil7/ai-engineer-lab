# Challenge 28 — Quiz: Code Quality Tooling

1. The mini linter must never execute the source; it works by:
   - A) importing it  (B) parsing with `ast.parse` and walking nodes  (C) eval  (D) regex only
2. Immutable defaults (`None`, `int`, `str`, `tuple`) are:
   - A) flagged as B006  (B) never flagged  (C) flagged as E722  (D) syntax errors
3. `E722` flags:
   - A) long lines  (B) bare `except:`  (C) mutable defaults  (D) complexity
4. Cyclomatic complexity counts:
   - A) lines  (B) 1 + decisions (`if`/`for`/`while`/`except`/`and`/`or`/ternary)  (C) functions  (D) imports
5. `analyze` must parse the source:
   - A) once per rule  (B) exactly once across all rules (measured)  (C) twice  (D) never
6. A `# noqa` comment suppresses a violation:
   - A) only with a rule code  (B) with or without a rule code  (C) never  (D) only in tests
7. A syntax error is reported as:
   - A) a crash  (B) `E999` at line 1, without crashing  (C) an empty dict  (D) `E501`
8. At 10^6 lines, what breaks first:
   - A) `ast.parse` (C-speed, fine)  (B) the per-node Python-level visit — why ruff is Rust  (C) disk I/O  (D) the noqa scan

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
