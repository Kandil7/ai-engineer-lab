# Challenge 26 — Quiz: Design Patterns Advanced

1. `__init_subclass__` registration happens:
   - A) at first instantiation  (B) at class-definition time  (C) at import of the base only  (D) manually
2. Hand-assigning `registry["calculator"] = Calculator` is forbidden because:
   - A) it is slower  (B) the point is declarative registration (a source check enforces it)  (C) dicts are immutable  (D) names collide
3. `registry_dispatch("unknown", {})`:
   - A) returns `""`  (B) raises `ValueError`  (C) returns `None`  (D) instantiates the base
4. `delete` must capture the removed text:
   - A) lazily at undo  (B) at construction, so undo restores the exact substring  (C) as a count only  (D) never
5. A new operation after `undo()`:
   - A) appends to the redo stack  (B) discards the redo history  (C) raises  (D) merges both
6. After `insert(0, "hello")`, `delete(0, 2)`, two `undo()` calls leave:
   - A) `"llo"`  (B) `""`  (C) `"hello"`  (D) `"he"`
7. `Summarizer` must receive `llm`:
   - A) as a global  (B) through its constructor (the signature check proves it)  (C) via a setter  (D) by subclassing
8. A Summarizer that constructs its client inside `__init__` fails because:
   - A) it is slower  (B) `inspect.signature` shows no `llm` parameter  (C) protocols reject it  (D) fakes cannot be built

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
