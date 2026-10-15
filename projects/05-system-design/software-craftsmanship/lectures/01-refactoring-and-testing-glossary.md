# Glossary 01: Refactoring and Testing

Quick-reference table of the 40 terms used in Lecture 01, followed by
full definitions with a DevMate or exercise example each. Every FACT
path cited here was verified before this track was written.

## Quick-Reference Table

| # | Term | One-line meaning |
|---|------|------------------|
| 1 | Refactoring | Behaviour-preserving restructuring under a green suite |
| 2 | Code smell | Surface hint that a deeper design problem exists |
| 3 | Extract method | Turn a code fragment into a named helper |
| 4 | Inline method | Fold a trivial helper back into its callers |
| 5 | Extract variable | Name an intermediate expression |
| 6 | Rename | Give a name that states intent |
| 7 | Replace conditional with polymorphism | Trade branches on a type code for competing types |
| 8 | Magic literal | Unexplained raw value repeated in logic |
| 9 | Introduce parameter object | Group a travelling trio of params into one type |
| 10 | Move method | Relocate a method to the data it envies |
| 11 | Decompose conditional | Split a tangled if into named condition and branches |
| 12 | Small-step discipline | Refactor in reversible steps with green checks between |
| 13 | Green suite | Every test passing; the license to restructure |
| 14 | Test pyramid | Many cheap unit tests, fewer integration, thin e2e top |
| 15 | Unit test | Fast deterministic check of one behaviour, no network |
| 16 | Integration test | Check across a real boundary, behind a marker |
| 17 | End-to-end test | Full journey through the live system, kept thin |
| 18 | Arrange-Act-Assert | Setup, single action, expectation structure for tests |
| 19 | One reason to fail | Each test diagnoses exactly one broken behaviour |
| 20 | Test double | Stand-in for a dependency in a test |
| 21 | Stub | Double that answers with canned data |
| 22 | Mock | Double that also verifies the interaction happened |
| 23 | Spy | Double that records calls for later assertion |
| 24 | Fake | Working lightweight implementation of a dependency |
| 25 | Seam | Boundary where behaviour can be substituted in tests |
| 26 | Mock at the seam | Place doubles at outside-world edges, never on internals |
| 27 | Property-based testing | Assert invariants over generated inputs |
| 28 | Mutation testing | Seed bugs to check the suite actually catches them |
| 29 | Mutant | One seeded bug a mutation run introduces |
| 30 | Kill rate | Share of mutants the suite catches |
| 31 | Code coverage | Share of code the suite executes; a floor, not a proof |
| 32 | Flaky test | Test that passes or fails without code changes |
| 33 | Wall-clock dependency | Read of real time that makes tests date-sensitive |
| 34 | Shared mutable state | Cross-test data that makes order matter |
| 35 | Test marker | Pytest label selecting which tests run in a gate |
| 36 | Golden test | Approved-output comparison against a fixed fixture |
| 37 | TDD | Write the failing test first, then the smallest fix |
| 38 | Regression test | Guard that a fixed bug stays fixed |
| 39 | Characterization test | Pin current behaviour before restructuring it |
| 40 | Deterministic test | Same code, same result, every run |

## Definitions

### 1. Refactoring

Restructuring the internals of code without changing its observable
behaviour, performed while the suite stays green so every step is
provably safe.

Example: renaming `price_a` to `price_with_tax` across the billing
module with the suite green before and after is a refactoring;
changing the rounding at the same time is not.

See also: Small-step discipline, Green suite.

### 2. Code smell

A surface pattern that suggests a design problem without proving one:
a long function, duplicated blocks, or a comment explaining what the
code does instead of why.

Example: three identical `audit("billing.retry")` lines are the smell;
the missing helper is the problem. Rule CRF002 flags the smell.

See also: Characterization test, Root cause versus symptom.

### 3. Extract method

Take a fragment that does one thing, move it into a named function,
and call it from the original site. The signal is a comment paragraph
or a block you want to name.

Example: the fee-capping lines inside `calculate_total` become
`cap_fee(subtotal)`; the BAD pack exists because nobody did this.

See also: Inline method, Decompose conditional.

### 4. Inline method

The reverse of extraction: fold a helper whose body no longer earns
its indirection back into its callers. Use it when a method only
delegates or its name duplicates the call.

Example: a `get_total` that only returns `self.total` can inline to
direct reads unless the seam needs the method for tests.

See also: Extract method, Move method.

### 5. Extract variable

Name an intermediate expression so the reader sees intent instead of
mechanics. The signal is a condition or formula you must re-read to
parse.

Example: `if (time - start) > budget and retries > 0` becomes
`expired = ...` and `can_retry = ...` before the `if`.

See also: Rename, Decompose conditional.

### 6. Rename

Choose the name that states intent: what the value means, what the
function guarantees, what the test proves. Renaming is the cheapest
refactoring and the most underused.

Example: `first`, `second`, `third` holding `"pending"` say nothing;
`queued_label` states the role. Rule CRF004 then has one constant.

See also: Magic literal, Extract variable.

### 7. Replace conditional with polymorphism

Replace a switch on a type code with competing types behind one
interface, each carrying its own branch. The signal is CRF003: three
or more branches testing the same attribute.

Example: `if order.status == "new" ... elif ...` becomes `NewOrder`,
`PaidOrder`, `SentOrder` strategies sharing `describe()`.

See also: Decompose conditional, Move method.

### 8. Magic literal

A raw string or number embedded in logic whose meaning only the
original author knew: `"pending"` in three places, `0.07` with no
name. Literal `0`, `1`, `None`, `True`, and `False` are exempt.

Example: the BAD pack repeats `"pending"` three times; the GOOD pack
binds `_ACTIVE_LABEL = "active"` once. Rule CRF004 flags repeats.

See also: Rename, Golden test.

### 9. Introduce parameter object

Group parameters that always travel together into one named type.
The signal is CRF007: the same three or more primitive params across
three or more signatures.

Example: `(customer_id, currency, precision)` on `price_a`, `price_b`,
and `price_c` becomes one `PricingContext`.

See also: Move method, Test double.

### 10. Move method

Relocate a method to the class holding the data it uses most, when it
envies another object's internals. The signal is a method reading
three fields of a neighbour and one of its own.

Example: receipt formatting that reads order fields exclusively moves
from the reporter onto the order type.

See also: Extract method, Replace conditional with polymorphism.

### 11. Decompose conditional

Split a tangled `if` into three named parts: the condition, the then
branch, the else branch. The signal is a condition spanning lines.

Example: the midnight-rollover guard becomes `is_rollover_window()`
with `freeze_clock()` and `advance_clock()` branches.

See also: Extract method, Wall-clock dependency.

### 12. Small-step discipline

Refactor as a chain of tiny reversible edits — extract, move, rename
— with a green check between each. Big-bang rewrites fail because no
single step is verifiable.

Example: replace the status switch by extracting one branch per
commit, running the suite each time, never mixing in fixes.

See also: Green suite, Characterization test.

### 13. Green suite

The state where every test in the gate passes. It is the license to
refactor: red means stop restructuring and restore green first.

Example: `.github/workflows/ci.yml:64-65` defines green for DevMate
as pytest passing with coverage; `:46-53` adds lint and format green.

See also: Regression test, Flaky test.

### 14. Test pyramid

The layering rule: many fast unit tests at the bottom, fewer
integration tests in the middle, a thin slow end-to-end top. Cost and
flakiness grow with height, so width belongs at the bottom.

Example: DevMate's `tests/unit/` files run in the default gate while
`tests/integration/test_services.py` needs live services.

See also: Unit test, Integration test, End-to-end test.

### 15. Unit test

A fast deterministic check of one behaviour with no network, no disk,
and no clock. It runs in milliseconds and fails only when the
behaviour breaks.

Example: `tests/unit/test_chunker.py` checks chunking purely in
memory; the exercise GOOD tests check `money` and `order_label`.

See also: Deterministic test, Arrange-Act-Assert.

### 16. Integration test

A check across one real boundary: database, queue, or service. Slower
and flakier than unit tests, so it sits higher in the pyramid and
behind a marker.

Example: `tests/integration/test_services.py` needs Qdrant and Redis
running and is excluded from the default addopts run.

See also: Test marker, Seam.

### 17. End-to-end test

A full user journey through the deployed system. Valuable and
expensive: slow, order-sensitive, and the first suite to flake, so the
pyramid keeps it thin.

Example: DevMate keeps live retrieval quality in the offline RAGAS
gate (`ci.yml:71-77`) rather than a heavy live e2e suite.

See also: Test pyramid, Flaky test.

### 18. Arrange-Act-Assert

The three-phase test shape: set up fixtures, perform one action,
check expectations. Blank lines or comments mark the phases so a
failure points at one cause.

Example: the GOOD tests carry `# arrange`, `# act`, `# assert`
markers; the BAD tests are one undifferentiated block. Rule TQ001.

See also: One reason to fail, Test double.

### 19. One reason to fail

The rule that each test diagnoses exactly one broken behaviour. A
test asserting three helpers has three reasons to fail and explains
none of them.

Example: `test_total_combined` asserts pricing, discount, and receipt
at once; the GOOD twins split one behaviour per test. Rule TQ003.

See also: Arrange-Act-Assert, Regression test.

### 20. Test double

Any stand-in for a dependency inside a test: stub, mock, spy, or
fake. Doubles isolate the unit from the outside world so failures
mean the unit broke.

Example: a canned exchange-rate table stands in for the rates API
while pricing logic is under test.

See also: Stub, Mock, Spy, Fake.

### 21. Stub

A double that answers with fixed data and verifies nothing. Use it
when the test needs the dependency to respond but not to be checked.

Example: a stub rate table always returns `1.08` so conversion math
is deterministic regardless of markets.

See also: Mock, Fake.

### 22. Mock

A double that answers and additionally verifies the interaction:
called once, with these arguments, in this order. Use it at seams
where the call itself is the behaviour.

Example: asserting the receipt sender was called once with the final
total, not just that some total was computed.

See also: Stub, Spy, Mock at the seam.

### 23. Spy

A double that records calls and arguments for assertions written
after the act phase. A mock asserts expectations up front; a spy
collects evidence first.

Example: a spy on the audit sink lets the test assert the exact retry
sequence after the billing run finishes.

See also: Mock, Fake.

### 24. Fake

A working but lightweight implementation: an in-memory queue, a dict
backed repository. Use it when the contract matters but the real
infrastructure is too heavy.

Example: an in-memory vector store with three fixed passages stands
in for Qdrant in a retrieval unit test.

See also: Stub, Integration test.

### 25. Seam

A place where behaviour can be substituted without editing the unit:
a constructor parameter, an imported client, the clock. No seam, no
isolation; the test must use the real thing.

Example: taking the rates client as a `money()` parameter creates a
seam; hard-coding the import inside the function removes it.

See also: Mock at the seam, Test double.

### 26. Mock at the seam

The placement rule: doubles sit where the unit meets the outside
world (network, clock, disk), never on internal helpers you own.
Mocking internals couples tests to implementation.

Example: patching `billing.price_a`, a pure internal helper, trips
rule TQ004; patching the HTTP client at the boundary is correct.

See also: Seam, Mock.

### 27. Property-based testing

Testing by asserting invariants over many generated inputs instead of
a few hand-picked cases: round-trips, idempotence, ordering. The
generator finds the edge case you would not write.

Example: chunk-then-rejoin equals the original text for any document;
discount never makes a total negative for any rate in range.

See also: Unit test, Mutation testing.

### 28. Mutation testing

Seeding small bugs into the code and checking the suite catches them.
A suite that stays green over broken code proves nothing; mutation
measures what coverage cannot.

Example: flipping `>` to `>=` in the fee cap must fail at least one
test, or the cap assertions are decorative.

See also: Mutant, Kill rate, Code coverage.

### 29. Mutant

One seeded defect in a mutation run: a flipped operator, a skipped
call, an off-by-one constant. Each mutant is a question the suite
must answer with a failure.

Example: changing `_DEFAULT_CURRENCY` to `"EUR"` is a mutant the
money tests must kill.

See also: Mutation testing, Kill rate.

### 30. Kill rate

The share of mutants the suite catches. High coverage with a low
kill rate means the suite executes code without checking it.

Example: 95 percent coverage with a 50 percent kill rate sends you
back to strengthen assertions, not to add more lines covered.

See also: Mutation testing, Code coverage.

### 31. Code coverage

The share of lines or branches the suite executes. Treat it as a
floor: below the bar something is untested; above it nothing is
proven about assertion strength.

Example: DevMate reports coverage with `--cov=devmate` in
`ci.yml:65` but gates quality separately through the eval thresholds.

See also: Kill rate, Regression test.

### 32. Flaky test

A test that passes or fails with no code change. Causes cluster into
time, randomness, ordering, and shared state; the fix is always at
the seam, never a retry loop around the suite.

Example: asserting exact LLM prose flakes on every model update;
midnight-only failures point at the clock seam.

See also: Wall-clock dependency, Shared mutable state.

### 33. Wall-clock dependency

Code that reads real time directly, making tests date-sensitive:
midnight rollovers, expiry math, timeout windows. Inject the clock or
freeze it.

Example: the midnight-CI failure disappears once the test passes a
fixed instant instead of calling the system clock.

See also: Flaky test, Seam.

### 34. Shared mutable state

Data one test writes and another reads: module-level caches, temp
files with fixed names, in-memory singletons. It makes pass order
decide results.

Example: two tests appending to one global basket see each other's
items; fixtures that build fresh state per test remove the coupling.

See also: Flaky test, Arrange-Act-Assert.

### 35. Test marker

A pytest label selecting which tests run where. DevMate registers
`integration` and `llm` and excludes both from the default addopts,
so unit tests gate every change and live tests gate deliberately.

Example: `pyproject.toml:112-120` sets `-m 'not integration and not
llm'`; `tests/integration/test_services.py` runs only on demand.

See also: Integration test, Unit test.

### 36. Golden test

A test comparing current output against an approved fixture: prompt
templates, serialized schemas, rendered receipts. The fixture is
reviewed once, then guards every later change.

Example: `tests/unit/test_prompt_golden.py` pins prompt output; the
GOOD billing tests pin `{"amount": 49, "currency": "EUR"}` exactly.

See also: Regression test, Deterministic test.

### 37. TDD

Test-driven development: write the failing test, watch it fail,
write the smallest fix, refactor while green. The honest role is
design feedback, not coverage generation after the fact.

Example: the missing `Precision` rounding rule gets a failing test
first; the implementation follows; the suite stays green throughout.

See also: Characterization test, Small-step discipline.

### 38. Regression test

A test added alongside a fix that pins the bug shut: it fails on the
old code and passes on the new. Every production incident should
leave one behind.

Example: after the midnight rollover fix, a test with a frozen
23:59 instant guards the boundary forever.

See also: Characterization test, Golden test.

### 39. Characterization test

A test written to pin current behaviour before restructuring it,
assertions first and judgment later. It turns unknown code into
known code so refactoring has a net.

Example: before replacing the status switch, pin each branch output
with golden assertions; refactor only while they hold.

See also: Regression test, Small-step discipline.

### 40. Deterministic test

A test with identical results on every run: seeded randomness, fixed
clocks, in-memory doubles, no network. Non-determinism in a unit
test is a defect in the test, not in the code.

Example: `tests/unit/test_cost.py` computes budgets from fixed
inputs; chunking and scoring tests never touch the model.

See also: Flaky test, Unit test.

*AI Engineer Lab — System Design track, software-craftsmanship lane.*
