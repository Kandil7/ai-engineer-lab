# Challenge 20: Patterns — The Gateway

An AI gateway fronts two providers. It normalizes each provider's request
shape, fans eval-run events out to subscribers, and routes every request to a
model tier under cost and latency budgets — the topic's patterns applied to
infrastructure you actually ship.

## Bronze — Provider Adapter (~15 min)

**Task:** Implement `adapt(provider, model, prompt, max_tokens)` returning the
provider's request dict. Provider names are exact lowercase identifiers;
anything else raises `ValueError`, as does `max_tokens < 1`.

**Signature:**
```python
def adapt(provider: str, model: str, prompt: str, max_tokens: int) -> dict
```

| Input | Expected |
|---|---|
| `("openai", "gpt-4o-mini", "hi", 128)` | `{"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 128}` |
| `("ollama", "llama3.2", "hi", 64)` | `{"model": "llama3.2", "prompt": "hi", "options": {"num_predict": 64}}` |
| `("openai", "m", "", 1)` | `{"model": "m", "messages": [{"role": "user", "content": ""}], "max_tokens": 1}` |
| `("cohere", "m", "hi", 8)` | `ValueError` |
| `("openai", "m", "hi", 0)` | `ValueError` |

**Constraints:** no network, no SDK imports. Any correct approach passes —
this tier is mechanics.

---

## Silver — Eval Event Bus (~35 min)

**Task:** Implement `EventBus` with `subscribe`, `unsubscribe`, `publish`.

- `subscribe(topic, handler)` registers a handler; a repeat of the same
  `(topic, handler)` pair is a no-op.
- `publish(topic, payload)` calls every handler for that topic in
  subscription order with the *same* payload object and returns how many
  handlers ran; an unknown topic returns `0`.
- `unsubscribe(topic, handler)` returns `True` when it removed the handler,
  `False` otherwise.

**Signature:**
```python
class EventBus:
    def subscribe(self, topic: str, handler: Callable[[dict], None]) -> None: ...
    def unsubscribe(self, topic: str, handler: Callable[[dict], None]) -> bool: ...
    def publish(self, topic: str, payload: dict) -> int: ...
```

| Scenario | Expected |
|---|---|
| one subscriber, publish | handler runs, returns `1` |
| two subscribers, one topic | insertion order, returns `2` |
| duplicate subscribe | handler still runs once, returns `1` |
| publish unknown topic | returns `0` |
| unsubscribe, then publish | `True`, then `0`; second unsubscribe `False` |

**Guard (measured):** the test registers 300 topics and publishes 300 times
using string objects that count their own comparisons. A flat
`(topic, handler)` list re-compares every stored topic on every publish —
about 90,000 comparisons — and fails the budget of `6 * (subscriptions +
publishes)`. A topic-indexed bus touches each key a constant number of times
and lands near 300. Structure, not speed.

---

## Gold — Tier Router (~75 min)

**Task:** Implement `ModelRouter`. It owns a candidate list and a probe
callable — `probe(name) -> {"p50_ms": float}` — and must honor one production
rule: **each model is probed at most once for the router's lifetime; total
probe calls never exceed `len(models)`.**

`route(...)` filters candidates by the constraints (`None` = unbounded), then
applies `strategy`:

| strategy | picks | tie-break |
|---|---|---|
| `"cheapest"` | lowest `cost_per_1k_cents` | name ascending |
| `"fastest"` | lowest probed `p50_ms` | name ascending |
| `"highest_quality"` | highest `quality` | name ascending |

No feasible model raises `ValueError`, as does an unknown strategy. Models
are `{"name": str, "cost_per_1k_cents": float, "quality": float}`; probed
latency arrives from the probe, not the model dict.

**Signature:**
```python
class ModelRouter:
    def __init__(self, models: list[dict], probe: Callable[[str], dict]) -> None: ...
    def route(
        self, *, max_cost_cents: float | None, max_latency_ms: float | None, strategy: str
    ) -> str: ...
```

Reference data: `a` costs `1.0` quality `0.7`, `b` costs `1.0` quality `0.9`,
`c` costs `4.0` quality `0.95`; probed p50 is `a: 120`, `b: 80`, `c: 40`.

| Scenario | Expected |
|---|---|
| `cheapest`, no constraints | `"a"` (cost tie with `b`, name wins) |
| `fastest`, no constraints | `"c"` (p50 40) |
| `highest_quality`, no constraints | `"c"` (0.95) |
| `cheapest`, `max_cost_cents=2`, `max_latency_ms=100` | `"b"` (only feasible) |
| `fastest`, `max_latency_ms=60` | `"c"` (only feasible) |
| `cheapest`, `max_cost_cents=0.5` | `ValueError` |
| `strategy="popular"` | `ValueError` |
| `models=[]` | any route raises `ValueError` |

**Guard (measured):** the fake probe raises the second time it sees a name,
and the test asserts `len(probe.calls) <= len(models)` after 60 mixed routes.
Re-probing on every route for fresher latency — same answers, wrong
economics — fails immediately.

---

## Follow-up

At 10^9 routes, what breaks first: the probe budget or the snapshot? Describe
the refresh policy you would ship (TTL? per-model interest? circuit breaker?)
and what it costs the night a model's p50 doubles. *(Answer sketch: staleness
breaks first — the budget only caps calls, it says nothing about freshness.
Key probes by model with a TTL and refresh out of band; the cost is one
stale window of latency-based routing, bounded by the TTL, not one probe
per request.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/20-patterns/test_challenge.py -q
# validate the reference solution:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/20-patterns/test_challenge.py -q
```

## Test File Structure

```
challenges/20-patterns/
├── README.md          # This file
├── starter.py         # Signatures only, bodies raise NotImplementedError
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
