# Challenge 27 — Quiz: Packaging and Distribution

1. `"1.2.0rc1".split(".")` breaks because `int("0rc1")` raises, so you must:
   - A) strip zeros  (B) partition the `rc` suffix before splitting  (C) use regex  (D) eval it
2. A final version with no pre-release gets the sentinel `2**63` so that:
   - A) it sorts before rcs  (B) finals sort after their pre-releases  (C) hashing works  (D) padding is skipped
3. `parse_version("1.26")` zero-pads to:
   - A) `(1, 2, 6, BIG)`  (B) `(1, 26, 0, BIG)`  (C) `(1, 26, BIG)`  (D) raises
4. Comparing version *strings* is wrong because:
   - A) strings are immutable  (B) `"1.10.0" < "1.9.9"` lexicographically  (C) locales differ  (D) of unicode
5. `compare_versions("1.26", "1.26.0")` returns:
   - A) 1  (B) 0 (PEP 440 zero-padding)  (C) -1  (D) raises
6. Following pip's default, `1.2.0rc1` satisfies `">=1.1"`:
   - A) yes  (B) no — a spec that never mentions a pre-release token excludes it  (C) only on Windows  (D) only with `--pre`
7. `max(available)` on version strings returns `"1.9.9"` where the resolver must return:
   - A) `"1.10.0"`  (B) `"2.0.0rc1"`  (C) `None`  (D) `"1.9.9"`
8. Between `"1.2.0rc1"` and `"1.2.0"`, `latest_compatible` picks:
   - A) the rc  (B) the final (rc < its own final)  (C) both  (D) neither

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-A, 8-B
