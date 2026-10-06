# Challenge 39 — Quiz: Poetry

1. `expand_constraint("1.2.3")` returns:
   - A) `(">=1.2.3", "<2.0.0")`  (B) `("==1.2.3", "")` — bare is exact  (C) `("", "")`  (D) raises
2. `expand_constraint("^0.2.3")` upper bound is:
   - A) `<2.0.0`  (B) `<0.3.0` (leftmost non-zero digit is the minor)  (C) `<0.2.4`  (D) unbounded
3. `expand_constraint("!=1.2.3")`:
   - A) returns the pair  (B) raises `ValueError` (unsupported in the teaching expander)  (C) returns `("", "")`  (D) returns `("!=1.2.3", "")`
4. `install_closure` on a cycle `A -> B -> A`:
   - A) loops forever  (B) terminates, returning `["A", "B"]`  (C) raises  (D) returns `[]`
5. With the root at the END of a 2000-package chain, a list-scan lookup:
   - A) passes  (B) is O(n²) and fails the comparison budget — index once  (C) is O(n)  (D) is cached
6. Editing `[tool.ruff] line-length` makes the lockfile:
   - A) stale  (B) still fresh — tool config is not part of the hashed content  (C) invalid  (D) regenerated
7. Adding a dependency to `[project]` makes `fresh`:
   - A) `True`  (B) `False` (the content hash changes)  (C) undefined  (D) irrelevant
8. The fetch budget rejects the natural two-loop audit because it:
   - A) is too slow  (B) fetches every direct package twice — fetch once into a cache, then sum  (C) sorts floats  (D) misses transitive deps

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
