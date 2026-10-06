# Challenge 23 — Quiz: Typing Advanced

1. In `build_schema`, a parameter without a default gets:
   - A) `""`  (B) `None`  (C) omitted  (D) `inspect.Parameter.empty`
2. The return annotation is recorded as:
   - A) the type object  (B) the stringified annotation  (C) always `"None"`  (D) a Protocol
3. `signature_matches(func, ["b", "a"])` is `False` because:
   - A) names are sorted first  (B) order matters  (C) defaults differ  (D) annotations differ
4. Parameter *names* are the robust runtime signal because:
   - A) they are unique  (B) annotations are stringified and unreliable to compare  (C) names are hashed  (D) types are erased
5. `@runtime_checkable` isinstance checks only see:
   - A) signatures  (B) member existence  (C) return types  (D) MRO
6. `WrongSignatureRetriever` proves the trap: `isinstance(obj, Retriever)` is `True` while `verify_retriever(obj)` is:
   - A) `True`  (B) `False` (the explicit signature check catches it)  (C) raises  (D) `None`
7. The naive isinstance-only check fails because it:
   - A) is slow  (B) accepts the wrong-shape class  (C) needs a metaclass  (D) caches badly
8. `safe_search` with a non-retriever argument:
   - A) raises  (B) returns `Result.failure` (fails gracefully)  (C) returns `None`  (D) retries

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
