# 🔬 Phase 2: Advanced Python

39 self-contained topic directories covering advanced Python concepts from decorators to production engineering, plus practice challenge sets for the production topics.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
02-advanced-python/
├── 01-decorators/
│   ├── 01-decorators.py
│   ├── 01-decorators-lecture.md
│   └── 01-decorators-glossary.md
├── 02-generators/
│   ├── 02-generators.py
│   ├── 02-generators-lecture.md
│   └── 02-generators-glossary.md
└── ... (39 topics)
```

Challenge sets (Bronze/Silver/Gold; the full index of all 21 sets lives in
`challenges/README.md`):

```
challenges/
├── README.md                                 # full index (01 stub, 20, 21–39)
├── 20-patterns/                              # adapter, observer bus, strategy router
├── 21-concurrency-comparison/ … 34-debugging-techniques/   # 14 sets, see index
├── 35-unicode-and-arabic-text/               # Bronze/Silver/Gold + quiz
├── 36-separation-of-concerns/
├── 37-code-review-and-refactoring/
├── 38-test-strategy-contract-regression/
└── 39-poetry/                                # Bronze/Silver/Gold
```

## 📚 Topics

| # | Topic | Description |
|---|-------|-------------|
| 01 | Decorators | Basic/class decorators, argument passing, stacking, caching |
| 02 | Generators | Yield, pipelines, send(), infinite sequences, memory efficiency |
| 03 | Context Managers | with statement, contextlib, resource management |
| 04 | Async/Await | asyncio, tasks, semaphores, producer-consumer |
| 05 | Type Hints | Annotations, generics, protocols, TypeVar |
| 06 | Dataclasses | Fields, frozen classes, inheritance, serialization |
| 07 | Enums | Auto values, flags, string enums, methods |
| 08 | ABCs | Interfaces, plugins, mixins, collections |
| 09 | Functools | reduce, partial, lru_cache, total_ordering |
| 10 | Itertools | Combinatorics, groupby, chaining, infinite iterators |
| 11 | Collections | Counter, defaultdict, namedtuple, deque, ChainMap |
| 12 | Properties | Getters/setters, caching, validation, computed values |
| 13 | Slots | Memory optimization, performance benchmarks |
| 14 | Metaclasses | Custom metaclasses, registries, singletons |
| 15 | Descriptors | __get__, __set__, validation, computed attributes |
| 16 | Threading | Threads, locks, semaphores, thread pools |
| 17 | Multiprocessing | Processes, pools, shared state, parallel computing |
| 18 | Unit Testing | unittest, mocking, fixtures, parameterized tests |
| 19 | Logging | Levels, handlers, formatters, application logging |
| 20 | Design Patterns | Singleton, Factory, Observer, Strategy, Adapter |
| 21 | Concurrency Comparison | Threads vs processes vs async, measured |
| 22 | Asyncio Advanced | TaskGroup, cancellation, shield, timeouts, queues |
| 23 | Typing Advanced | Protocol, ParamSpec, TypeGuard, generics, bounds |
| 24 | Memory & GC | Refcounts, cycles, weak refs, slots, tracemalloc |
| 25 | Profiling & Optimization | timeit, cProfile, hash join, memoization, vectorization |
| 26 | Design Patterns Advanced | Adapter, DI, Command, Registry, Strategy |
| 27 | Packaging & Distribution | pyproject.toml, semver, PEP 440, extras, entry points |
| 28 | Code Quality Tooling | Linters, formatters, type checkers, pre-commit |
| 29 | Functional Python | map, filter, reduce, lambdas, functional patterns |
| 30 | Iterators & Protocols | __iter__, __next__, protocol design, lazy evaluation |
| 31 | Concurrency Patterns | Producer-consumer, work stealing, actor model |
| 32 | Metaprogramming | exec, eval, code generation, AST manipulation |
| 33 | Security Essentials | Input validation, secrets, CORS, rate limiting |
| 34 | Debugging Techniques | pdb, breakpoints, logging, profiling |
| **35** | **Unicode & Arabic Text** | Code points vs bytes, NFC/NFKC, presentation forms, harakat, digit folding, batch import with located errors |
| **36** | **Separation of Concerns** | Layered pipeline, Protocols, DI, composition root, frozen config, engine-swap proof |
| **37** | **Code Review & Refactoring** | Review lenses, smell measurement (ast), extract-method, lock tests, four-part comments |
| **38** | **Test Strategy** | Unit/integration/contract/regression/data tests, provenance, idempotency, golden cases |
| **39** | **Poetry** | Constraints (^, ~, ~=), group selection, content-hash freshness, lockfile audit, index-fetch budget |

## 🚀 Quick Start

```bash
# Run any topic
python 01-decorators/01-decorators.py

# Run all topics
for d in [0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done

# Verify a challenge set (starter fails until solved)
python -m pytest challenges/35-unicode-and-arabic-text/test_challenge.py -q
# Validate the reference solution:
#   $env:CHALLENGE_USE_SOLUTION = "1"  (PowerShell)
python -m pytest challenges/35-unicode-and-arabic-text/test_challenge.py -q
```

## 📖 Recommended Learning Order

### Beginner-Intermediate (01-12)
1. **01-decorators** - Essential for understanding Python's power
2. **02-generators** - Memory-efficient iteration
3. **05-type-hints** - Modern Python best practices
4. **06-dataclasses** - Clean class definitions
5. **12-property** - Attribute management

### Intermediate (03-11, 13-20)
6. **03-context-managers** - Resource management
7. **07-enum** - Constants and states
8. **08-abc** - Interface design
9. **09-functools** - Functional programming tools
10. **10-itertools** - Efficient iteration patterns
11. **11-collections** - Specialized containers

### Advanced (13-20, 04)
12. **13-slots** - Memory optimization
13. **14-metaclasses** - Class creation control
14. **15-descriptors** - Attribute access customization
15. **16-threading** - Concurrent programming (I/O-bound)
16. **17-multiprocessing** - Parallel programming (CPU-bound)
17. **18-unit-testing** - Testing best practices
18. **19-logging** - Application logging
19. **20-patterns** - Design patterns in Python
20. **04-async-await** - Async programming (most complex)

### Production Depth (21-34)
21-34. Advanced topics for production applications

### Production Engineering (35-38) — Athar mastery track
35. **35-unicode-and-arabic-text** — Arabic corpus hygiene and the streaming importer
36. **36-separation-of-concerns** — swappable search engine, validation independence
37. **37-code-review-and-refactoring** — structure measured, behavior locked
38. **38-test-strategy-contract-regression** — the five test types on one pipeline

These four map directly to the Athar skills table — see
[`../SKILLS_MASTERY_MAP.md`](../SKILLS_MASTERY_MAP.md). Each has a challenge set
in `challenges/` with Bronze/Silver/Gold tiers.

### Tooling (39)
39. **39-poetry** — dependency management: constraint expansion, lockfile verification, manifest audit

## 🎯 Each Topic Contains

- **3-5 complete working examples** with real implementations
- **Output comments** showing expected results
- **Progressive difficulty** within each topic
- **Practical use cases** for real-world applications
- **Self-contained directory** with exercise, lecture, and glossary

---

*Last updated: September 2026*
