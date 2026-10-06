# 02-advanced-python — Challenge Sets

Practice sets follow [`PRACTICE_SPEC.md`](../../PRACTICE_SPEC.md): Bronze (mechanics)
→ Silver (right structure, measured guard) → Gold (production constraint).

| Challenge | Topic | Skills |
|---|---|---|
| `01-decorators/` | [Decorators](../01-decorators/) | *stub — `starter.py` only, no solution or tests yet* |
| `20-patterns/` | [Patterns](../20-patterns/) | provider adapter, observer bus, strategy router with probe budget |
| `21-concurrency-comparison/` | [Concurrency Comparison](../21-concurrency-comparison/) | concurrency model choice, I/O overlap measurement, CPU parallelism |
| `22-asyncio-advanced/` | [Asyncio Advanced](../22-asyncio-advanced/) | semaphore caps, bounded pipeline with backpressure, batch orchestration |
| `23-typing-advanced/` | [Typing Advanced](../23-typing-advanced/) | signature introspection, runtime contract checks, typed retriever |
| `24-memory-and-gc/` | [Memory and GC](../24-memory-and-gc/) | cycle collection, honest instance sizing, weakref cache with a tracer |
| `25-profiling-and-optimization/` | [Profiling and Optimization](../25-profiling-and-optimization/) | scan removal, order-preserving dedup, memoization by call count |
| `26-design-patterns-advanced/` | [Design Patterns Advanced](../26-design-patterns-advanced/) | tool registry, undoable editor, constructor-injection signature check |
| `27-packaging-and-distribution/` | [Packaging and Distribution](../27-packaging-and-distribution/) | PEP 440 versions, requirement specifiers, version resolution |
| `28-code-quality-tooling/` | [Code Quality Tooling](../28-code-quality-tooling/) | mini linter on the `ast` module, zero-dependency CI checks |
| `29-functional-python/` | [Functional Python](../29-functional-python/) | cacheable pure pipeline, memoized transforms, replay determinism |
| `30-iterators-protocols-deep/` | [Iterators and Protocols](../30-iterators-protocols-deep/) | dunder container, `collections.abc` base, ABC protocol checks |
| `31-concurrency-patterns/` | [Concurrency Patterns](../31-concurrency-patterns/) | rate limiting, bounded producer-consumer, circuit breaker |
| `32-metaprogramming/` | [Metaprogramming](../32-metaprogramming/) | `__init_subclass__` registration, signature-derived schemas, plugins |
| `33-security-essentials/` | [Security Essentials](../33-security-essentials/) | timing-safe verify, salted PBKDF2, SQL injection resistance |
| `34-debugging-techniques/` | [Debugging Techniques](../34-debugging-techniques/) | full-stack logging, boundary-asserting debugger, deterministic replay |
| `35-unicode-and-arabic-text/` | [Unicode and Arabic Text](../35-unicode-and-arabic-text/) | normalization, streaming import, located errors |
| `36-separation-of-concerns/` | [Separation of Concerns](../36-separation-of-concerns/) | Protocols, DI, engine-swap invariant |
| `37-code-review-and-refactoring/` | [Code Review and Refactoring](../37-code-review-and-refactoring/) | smell measurement, lock tests, structural budgets |
| `38-test-strategy-contract-regression/` | [Test Strategy](../38-test-strategy-contract-regression/) | provenance, idempotency, regression gate |
| `39-poetry/` | [Poetry](../39-poetry/) | constraint expansion, group selection, lockfile audit |
| `40-uv/` | [uv](../40-uv/) | wheel-tag selection, indexed wheel queries, streaming lock audit |

## Running

```powershell
python -m pytest 02-advanced-python/challenges/<name>/test_challenge.py -q
# validate the reference solution:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/<name>/test_challenge.py -q
```

Default runs target `starter.py` and fail with `NotImplementedError` until solved.
