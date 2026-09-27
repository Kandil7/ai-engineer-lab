# Separation of Concerns Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Concern | A single reason the code changes (parsing, rules, search, API) |
| Separation of concerns | Design rule: one module per reason to change |
| Layer | A stage of processing that speaks in plain data to its neighbors |
| Single responsibility | A unit does one job and has one axis of change |
| God object/function | Unit fused with many concerns; every change is high-risk |
| Contract | The exact methods a collaborator must provide |
| Protocol (typing) | Structural interface: matching methods = conformance, no inheritance |
| `@runtime_checkable` | Enables `isinstance` checks against a Protocol |
| Duck typing | Python's native structural typing ("has the methods") |
| ABC | Abstract base class; explicit inheritance-based interface |
| Liskov substitution | A substitute must honor the original's contract fully |
| Dependency injection | A component receives collaborators instead of constructing them |
| Constructor injection | Dependencies passed via `__init__` (preferred form) |
| Composition root | The single place that names concrete classes and wires them |
| Factory function | Function like `make_pipeline()` that assembles the graph |
| Service locator | Anti-pattern: hidden registry that dependencies are pulled from |
| Config object | Immutable dataclass holding settings, passed down explicitly |
| Frozen dataclass | `frozen=True` — mutation raises `FrozenInstanceError` |
| Pure function | No I/O, no globals; same input → same output |
| Side effect | Observable change outside the return value (I/O, mutation, logs) |
| Spy / test double | Fake collaborator that records calls for assertions |
| ParseError | Typed failure: input could not be read structurally |
| ValidationError | Typed failure: readable input breaks a business rule |
| Quarantine | Skip-and-log policy for bad records instead of aborting |
| Reason to change | The maintenance trigger a module is sensitive to |
| Seam | A point where behavior can be substituted (where a Protocol lives) |
| Blast radius | Code that must change or re-test when one thing changes |
| Named logger | `logging.getLogger(__name__)`; app configures handlers, not libraries |
| Library vs application code | Library exports behavior; application owns wiring and config |

---

## Detailed Definitions

### Concern and separation of concerns
A concern is a reason the code changes. Separating them means a retrieval experiment never touches reference rules, and a rules change never touches the search engine. The audit: finish "I edit this file when ___ changes" — two different answers mean split the module.

### Contract and Protocol
A contract is the exact behavior a collaborator must provide. `typing.Protocol` expresses it structurally: any class with matching methods conforms, no inheritance required. Keep contracts minimal so alternative implementations stay cheap.

### Dependency injection and composition root
Collaborators arrive via the constructor instead of being constructed inside. Concrete classes are named only at the composition root (a factory like `make_pipeline`). Tests inject spies; production injects real engines.

### Configuration object
Settings modeled as a frozen dataclass built once at startup and passed down. Avoids untestable deep `os.environ` reads and cross-test mutation of module globals.

### Pure functions vs side effects
Normalization logic is pure (same input, same output, no I/O): trivially testable. I/O and logging live at the edges. Splitting impure edges from pure middle is the core layering move.

### Typed errors and quarantine
`ParseError` (can't read) and `ValidationError` (breaks a rule) let callers apply different failure policies. Quarantine = skip the bad record, log it with its identifier, continue the run.

### Spy double and engine-swap test
The spy records every call through a Protocol to prove the pipeline never bypasses its contract. The engine-swap test runs identical input through two engines and asserts identical validation outcomes — the mechanical proof that rules are independent of retrieval.

### Reason to change / blast radius
The maintenance axis a module serves, and the amount of code that must re-test when it moves. Good separation shrinks blast radius to one module per change.

### Library vs application code
Library code exports behavior, uses named loggers, and never configures handlers or reads env vars. Application code owns logging setup, config loading, and wiring.
