# Challenge 29 — Quiz: Functional Python

1. `square_evens` must build its result with:
   - A) a comprehension  (B) `map` + `filter`  (C) a loop with append  (D) recursion
2. After `square_evens(nums)`, the caller's list is:
   - A) mutated  (B) unchanged (purity is asserted)  (C) sorted  (D) emptied
3. `compose(g, f)(x)` computes:
   - A) `f(g(x))`  (B) `g(f(x))`  (C) `g(x) + f(x)`  (D) `f(x)`
4. `memoize` is pure because it changes:
   - A) results  (B) only the cost, never the results  (C) the signature  (D) the module
5. The memo test proves caching by asserting the second call with the same argument:
   - A) is faster  (B) does not re-invoke the wrapped function  (C) returns `None`  (D) raises
6. `pipeline([1, -2, 3])` (normalize, double, square) returns:
   - A) `[1, 4, 9]`  (B) `[4, 0, 36]`  (C) `[2, -4, 6]`  (D) `[0, 0, 0]`
7. `steps_fingerprint` must differ when:
   - A) data changes  (B) the same steps appear in a different order  (C) the cache grows  (D) nothing
8. With unhashable items in `data`, the fingerprint must:
   - A) raise  (B) serialize or tuple-ify them (lists to tuples, dicts to sorted-item tuples)  (C) skip caching  (D) hash the id

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
