# Challenge 20 — Quiz: Patterns

1. `adapt("OpenAI", "m", "hi", 8)` raises:
   - A) nothing  (B) `ValueError` (exact lowercase names)  (C) `KeyError`  (D) returns `{}`
2. Subscribing the same `(topic, handler)` twice, then publishing, runs the handler:
   - A) twice  (B) once (duplicate is a no-op)  (C) zero times  (D) raises
3. `publish` on a topic with no subscribers returns:
   - A) `None`  (B) raises  (C) `0`  (D) `-1`
4. A flat `(topic, handler)` list bus fails the comparison budget because:
   - A) strings are slow  (B) every publish re-compares every stored topic (~90,000 vs 3,600)  (C) dicts are faster  (D) handlers are hashed twice
5. `unsubscribe` on a handler that was never subscribed returns:
   - A) `True`  (B) raises  (C) `False`  (D) `None`
6. Two models tie on cost under `"cheapest"`; the winner is:
   - A) insertion order  (B) name ascending  (C) random but seeded  (D) higher quality
7. The router's probe budget exists so that:
   - A) latency is fresh every route  (B) each model is probed at most once per router lifetime  (C) probes run in parallel  (D) failures retry
8. Under `"fastest"`, latency comes from:
   - A) the model dict  (B) the probe callable  (C) a config file  (D) the strategy name

**Answers:** 1-B, 2-B, 3-C, 4-B, 5-C, 6-B, 7-B, 8-B
