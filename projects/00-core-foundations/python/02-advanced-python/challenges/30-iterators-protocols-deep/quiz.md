# Challenge 30 — Quiz: Iterators and Protocols Deep

1. A missing key in `KeyValueStore` must raise:
   - A) `None`  (B) `KeyError`  (C) `ValueError`  (D) nothing
2. With `__getitem__` + `__len__` + `__iter__`, `collections.abc.Mapping` supplies for free:
   - A) nothing  (B) `get`, `keys`, `values`, `items`, `__eq__`  (C) `__hash__`  (D) `__setitem__`
3. Implementing `get`/`keys` by hand is the wrong approach because:
   - A) it is slower  (B) the ABC must do the work (the test checks the MRO)  (C) names collide  (D) it breaks `len`
4. After `snapshot()`, mutating the source store:
   - A) changes the snapshot  (B) never changes the snapshot  (C) raises  (D) rehashes it
5. `SnapshotDict.__hash__` is computed:
   - A) on every access  (B) once at construction (O(n) once, O(1) after)  (C) never  (D) by the ABC
6. Value equality implies hash equality, so two equal stores:
   - A) hash differently  (B) hash identically  (C) cannot both be snapshotted  (D) raise
7. Mutating an object after using it as a dict key corrupts the dict because:
   - A) dicts rehash eagerly  (B) the stored hash no longer matches, so lookups miss and entries leak  (C) keys are copied  (D) gc intervenes
8. A snapshot is safe as a dict key because it is:
   - A) large  (B) immutable and hashable  (C) sorted  (D) a Mapping

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
