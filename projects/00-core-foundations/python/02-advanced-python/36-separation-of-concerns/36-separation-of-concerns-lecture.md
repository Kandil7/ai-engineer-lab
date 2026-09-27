# Advanced Python Lecture 36: Separation of Concerns and Maintainable Architecture

## Topic Overview

A working prototype proves the idea; a maintainable system survives the idea changing. The single most useful maintenance metric in a reference system like Athar is this: **can you replace the search engine without re-certifying the reference-validation rules?** If the answer is no, the two concerns are fused in the code and every retrieval experiment risks corrupting correctness. This lecture builds the discipline that prevents it: one job per module, contracts expressed as Protocols, dependencies injected at a single composition root, configuration as data, and logging that a library never owns. The final section is the mastery test itself — a pipeline where the search backend is swapped while the validator, its tests, and its rules remain bit-identical.

The theme: **architecture is the set of decisions you can change cheaply.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Split a mixed pipeline into layers with one responsibility each.
2. Define a contract with `typing.Protocol` and verify implementations structurally.
3. Inject dependencies through constructors and keep concrete classes at one root.
4. Model configuration as an immutable dataclass instead of global/env reads.
5. Apply library-grade logging rules (named loggers, no handler config, no `print`).
6. Prove with a spy double that a component only talks to its contract.
7. Run the engine-swap test and explain why validation rules are provably untouched.

---

## Prerequisites

| Need | Where |
|---|---|
| Dataclasses | `06-dataclasses-lecture.md` |
| Abstract base classes | `08-abc-lecture.md` |
| Logging basics | `19-logging-lecture.md` |
| Exceptions design | `47-exceptions-advanced-lecture.md` |
| Normalization pipeline | `35-unicode-and-arabic-text-lecture.md` |

---

## 1. What "separation of concerns" actually means

A **concern** is a reason the code changes:

| Concern | Changes when… | Athar example |
|---|---|---|
| Parsing | a source format changes | JSONL → XML feed |
| Normalization | Arabic text rules change | new diacritic folding policy |
| Validation | reference scholarship rules change | page ranges per edition |
| Indexing | retrieval technology changes | substring → BM25 → vector |
| API | product surface changes | `/search` gains filters |

The rule is not "one class per noun" — it is **one reason to change per module**. When a retrieval experiment forces a change in `validate_record`, the layers are fused and the experiment is unsafe. When a rule change ("pages must be positive") touches nothing in the search engine, the separation is real.

The standard test is the **reason-to-change audit**: for each function, finish the sentence "I would edit this file when ___ changes." If two unrelated answers fit, split it.

## 2. Layering the pipeline

The shape used throughout this course — and in the exercise — is a one-directional flow of plain data:

```
raw bytes/lines  --parse-->  RawRecord  --validate-->  ValidatedRecord  --index-->  SearchIndex
```

Three properties make it cheap to maintain:

1. **Each layer speaks only in data structures** (dataclasses), not in each other's objects. The validator does not receive a parser — it receives a `RawRecord`.
2. **Errors are typed per layer**: `ParseError` (can't read it) vs `ValidationError` (read it, but it breaks a rule). The caller can treat them differently: parse errors usually quarantine the file; validation errors usually quarantine the record.
3. **Pure middle, impure edges**: parsing touches I/O, normalization is a pure function, indexing touches storage. Keeping the middle pure makes the hard logic trivially testable.

Anti-pattern to recognize: the *god pipeline* — one function that loads the file, cleans text, checks rules, opens a connection, indexes, and returns the HTTP response. Every one of those five reasons to change is in one blast radius.

## 3. Contracts with `typing.Protocol`

A **Protocol** describes behavior structurally: any class with the right methods *is* the contract — no inheritance needed. This is Python's interface mechanism and it is strictly better than ABCs for pluggable collaborators, because implementations need not know the contract exists.

```python
@runtime_checkable
class SearchIndex(Protocol):
    def add(self, record: ValidatedRecord) -> None: ...
    def search(self, query: str, limit: int = 5) -> list[ValidatedRecord]: ...
```

`@runtime_checkable` adds `isinstance(x, SearchIndex)` — method-presence checking only, which is enough to catch wiring mistakes at startup. Static checkers (mypy/pyright) verify call sites and implementations at compile time.

Why the contract must be **small**: `add` and `search` are the entire surface. A contract with fifteen methods forces every alternative engine to implement fifteen things and makes the "swap" promise a lie. Keep the seam narrow.

ABCs still have a place — when you want to share implementation (a `BaseIndex` with common logging) — but for *substitutability*, Protocols are the tool.

## 4. Dependency injection

**Dependency injection** means a component receives its collaborators instead of constructing them. The payoff is the substitution the mastery test needs:

```python
class Pipeline:
    def __init__(self, index: SearchIndex, cfg: PipelineConfig) -> None:
        self._index = index
        self._cfg = cfg
```

`Pipeline` cannot see `InMemoryIndex`. It sees `SearchIndex`. When the constructor names only contracts, a test can pass a `SpyIndex` and assert exactly what the pipeline did — the verification section does precisely this.

The **composition root** is the single place where concrete classes are named:

```python
def make_pipeline(engine: str = "memory") -> Pipeline:
    index: SearchIndex = InMemoryIndex() if engine == "memory" else PrefixIndex()
    return Pipeline(index, config)
```

Rules of thumb:

- Concrete classes appear in exactly one module (the root) plus their own definition.
- No `isinstance` checks on collaborators inside business logic — if you need one, the contract is wrong.
- Constructor injection over setter/attribute injection: an object is complete or it fails to construct.
- Factories (`make_pipeline`) beat service locators and registries for a codebase this size.

## 5. Configuration as data

Two anti-patterns cause most config bugs: reading `os.environ` deep inside functions (untestable — two configurations can't coexist in one process) and mutable module-level dicts (one test changes it, the next inherits the damage).

The fix is a **frozen dataclass built once at startup** and passed down:

```python
@dataclass(frozen=True)
class PipelineConfig:
    strict_pages: bool = True
    min_text_length: int = 3
```

`frozen=True` makes mutation a `FrozenInstanceError` at the call site instead of a mystery two files away. Rules that *are* policy (are negative pages allowed?) read from config; they never hard-code a literal that an experiment might need to vary. The verification proves it: with `strict_pages=False`, the very same validator accepts what strict mode rejects — the rule didn't change, the configuration did.

Environment variables are read at the boundary (startup/main), converted to the config object, and never referenced again.

## 6. Library-grade logging

Logging has three rules that separate professional code from scripts:

1. **Libraries use named loggers and never configure handlers.** `logging.getLogger(__name__)` lets the application decide destinations and levels. `logging.basicConfig()` in a library hijacks the host application's logging.
2. **Never `print()` in library code.** Print cannot be silenced in tests, redirected to a file, or graded at WARNING. The only prints in this course are in the exercise demos themselves.
3. **Log at the right level**: DEBUG for developer detail, INFO for lifecycle events ("pipeline ready"), WARNING for skippable bad data (the quarantined record), ERROR for failures a human must act on. The quarantine log line — `WARNING ... skipping record: r3: page not numeric: 'x'` — is the audible form of the fail-loud policy from topic 35.

Log messages carry **identifiers** (`record_id`, `engine=`) so the log is greppable evidence, not prose.

## 7. Proving the separation

Architecture claims are worthless without a mechanical check. Two cheap proofs:

**The spy double** — implement the Protocol with a recorder and assert the pipeline's entire outside interaction:

```python
spy = SpyIndex()
Pipeline(spy, config).search("نص")
assert spy.queries == ["نص"]
```

If the pipeline reached around the contract (opened a real engine, called a module function), the spy would not see the call and the test fails.

**The engine-swap test** — run identical input through both engines and compare the *validation* outcomes:

```python
comp = run_both_engines(demo_lines)
assert comp["memory"]["errors"] == comp["prefix"]["errors"]
```

Equal error sets mean validation is a function of the record and config only — not of the engine. That is the exact claim the skills map demands: *replace the search engine without touching the reference rules.*

## 8. Where code review fits

Maintainability is enforced at review time. When reviewing a change, ask:

- Does each new function have exactly one reason to change?
- Does any business rule import a concrete I/O class (engine, client, connection)?
- Is a new config value a literal hidden in logic, or a field of the config object?
- Do errors carry the identifier a log reader needs?
- Can the change be tested without opening a socket?

If any answer is wrong, the review comment is about **structure**, not style — and it is cheaper to fix at review than after the first incident.

## 9. Best-practice checklist

| Practice | Payoff |
|---|---|
| One reason to change per module | changes stay in one blast radius |
| Plain dataclasses between layers | layers testable in isolation |
| Protocols for every collaborator | engine swap is a one-line wiring change |
| Small contracts | alternative implementations are cheap |
| One composition root | grep finds every concrete class instantly |
| Frozen config dataclass passed down | two configs can coexist in tests |
| Typed `ParseError` vs `ValidationError` | quarantine policy per failure class |
| Named loggers, no handler config in libs | host app owns log destinations |
| Spy-double test on the contract | proved, not assumed |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Endpoint function does parse+validate+index+respond | split into layers; endpoint calls one orchestrator |
| `if backend == "qdrant"` inside business logic | inject the backend; branch only at the root |
| Deep `os.environ` reads | one settings object built at startup |
| Config dict mutated by tests | `frozen=True` dataclass |
| Broad contract with 12 methods | shrink to what callers actually use |
| `print()` for progress in library code | named logger at INFO/WARNING |
| Validation logic inside the search engine | move rules to their own module |
| Untyped `ValueError` with no record id | typed error carrying identifiers |

---

## Mastery Check

You can claim this topic when you can:

1. Delete the search engine implementation and add a new one (e.g. a vector store) **without editing any validation code** — and the validator's tests still pass unchanged.
2. Point at one file that is the only place naming concrete collaborators.
3. Run two different configs in one test session with no interference.
4. Replace logging output with a handler capture in tests without touching library code.
5. Draw the data flow of a request and name the reason-to-change for each box.

---

## Next Steps

- Practice the review discipline in `37-code-review-and-refactoring-lecture.md`.
- Lock the layers with the test types in `38-test-strategy-contract-regression-lecture.md`.
- See the contract idea at system scale in `10-system-design/01-component-contracts/`.
