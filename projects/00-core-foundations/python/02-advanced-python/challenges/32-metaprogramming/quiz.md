# Challenge 32 — Quiz: Metaprogramming

1. Tool registration via `__init_subclass__` happens:
   - A) at instantiation  (B) at class-definition time, no metaclass needed  (C) at import of the registry  (D) via a decorator only
2. `Tool.registry` keys are:
   - A) lowercase names  (B) exact class names, base class excluded  (C) module paths  (D) ids
3. In the JSON schema, `list[str]` maps to:
   - A) `"list"`  (B) `"array"`  (C) `"string"`  (D) omitted
4. With `from __future__ import annotations`, annotations are strings at runtime, resolved via:
   - A) `eval`  (B) `typing.get_type_hints`  (C) `ast.parse`  (D) `__annotations__` directly
5. For methods, `schema_for` excludes:
   - A) defaults  (B) `self`/`cls`  (C) return types  (D) docstrings
6. An untyped parameter produces a property:
   - A) with `"type": "any"`  (B) with no `"type"` key  (C) that is skipped  (D) that raises
7. The `@tool` decorator must:
   - A) hand-write the schema  (B) derive the schema from the signature  (C) register only  (D) wrap with retries
8. `load_plugin` on the same module twice:
   - A) re-imports  (B) is cached by Python's import machinery  (C) raises  (D) leaks memory

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
