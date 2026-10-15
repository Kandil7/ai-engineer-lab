# Lecture 01: Refactoring and Testing for Working Engineers

## Topic Overview

Every codebase old enough to matter carries the same scar tissue:
functions that grew one urgent commit at a time, prompts pasted into
three call sites, branches on a status field that now needs a fourth
case, and a test suite that everyone fears and nobody trusts. There
are two disciplines that keep scar tissue from becoming permanent
damage. Refactoring restructures code without changing what it does,
and testing proves it still does it. This lecture teaches both as one
practice: the definition of refactoring and the green suite that
licenses it, the smell catalog including the new LLM-era smells, eight
catalog moves each with signal, steps, and safety, small-step
discipline and when not to refactor, root cause versus symptom, the
test pyramid with its LLM twist, what makes a test good, doubles and
seams, property-based and mutation testing with coverage in its honest
place, and the deterministic testing strategy DevMate runs in CI.
Claims labeled FACT were verified at the cited path in this
repository; everything else is general practice from the refactoring
and testing literature (Fowler 2018, Beck 2002).

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python functions, classes, and pytest basics; the
DevMate gate files cited below are read during the lecture, so no
setup is needed beyond a checkout of this repository

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Define** refactoring as behaviour-preserving restructuring under
   a green suite, and reject changes that mix restructuring with fixes
2. **Detect** classic and LLM-era smells, including 400-character
   inline prompts and helper-module dumping grounds
3. **Apply** eight catalog moves — extract and inline method, extract
   variable, rename, replace conditional with polymorphism, replace
   magic literals, introduce parameter object, move method, decompose
   conditional — each with its signal, steps, and safety check
4. **Practice** small-step discipline and state when refactoring is
   forbidden: red suites, live incidents, and unpinned behaviour
5. **Distinguish** root causes from symptoms so fixes land once
   instead of every sprint
6. **Layer** the test pyramid and explain the LLM twist: a wide cheap
   deterministic bottom and a thin expensive live top
7. **Write** tests that assert behaviour not implementation, shaped as
   Arrange-Act-Assert with one reason to fail
8. **Place** stubs, mocks, spies, and fakes at the seam, and define
   what counts as a seam in the first place
9. **Evaluate** a suite with property-based tests, mutation testing,
   and coverage held as a floor rather than a proof
10. **Audit** source and test packs against the twelve CRF/TQ rules
    and interpret every finding the exercise reports

---

## Key Concepts

### 1. Refactoring Means Behaviour-Preserving Change Under a Green Suite

A refactoring changes the internal structure of code without changing
its observable behaviour. The definition has two halves and both are
load-bearing. Behaviour-preserving means callers, outputs, and edge
cases stay identical: same totals, same errors, same ordering. Under
a green suite means the proof exists before the first edit, not as a
hope after the last one. The suite is a contract written in
assertions; green says the contract currently holds, and staying
green through every step says it still holds.

The practical test is the revert test. If a reviewer cannot tell from
the test results whether you refactored or did nothing, the change
qualifies. Renaming `price_a` to `price_with_tax` with green before
and green after is a refactoring. Renaming while also fixing the
rounding is two changes wearing one commit message, and when the
suite goes red nobody knows which half broke. FACT: DevMate defines
green mechanically — `projects/04-ai-engineering/devmate/pyproject.toml:112-120`
sets the default pytest run to `-m 'not integration and not llm'`, so
the unit gate is deterministic by construction, and
`.github/workflows/ci.yml:46-65` adds ruff check, ruff format check,
and mypy on `src/` before tests even run.

Two confusions must die here. Refactoring is not rewriting: a rewrite
discards behaviour and reimplements it, which is sometimes right but
is never safe by definition. Refactoring is not cleanup in the
aesthetic sense: formatting, comment fixes, and import sorting are
fine, but they are not the discipline this lecture teaches. The
discipline is structural improvement with a proof attached.

A concrete walkthrough makes the standard vivid. Suppose the billing
module computes fees with the rate `0.07` written inline in four
places. Step one: run the gate and confirm green. Step two: bind
`FEE_RATE = 0.07` at module scope and replace one occurrence, then
run the gate. Step three: replace the remaining three, one per edit,
gate after each. Step four: run the full gate once more and commit.
Four occurrences, five green checks, zero drama. Anyone reviewing
that commit sees only a name introduced and proves safety by running
one command. Contrast the shortcut: replace all four, rename two
functions, and fix the rounding in one diff. When that diff goes red,
the failure could be any of the three changes, and the reviewer must
reconstruct intent instead of verifying structure. The boring path is
faster because it never needs archaeology.

The workflow is therefore fixed. First get green, and if the suite is
red, stop: fix forward or revert, but do not restructure on red.
Then make one small structural change. Then run the gate again. The
loop is boring on purpose. Every famous refactoring disaster — the
month-long branch, the framework migration disguised as cleanup —
started by skipping one of these steps. Small and green is not slow;
it is the fastest speed at which restructuring stays safe.

### 2. Smells, Including the New LLM-Era Smells

A smell is not a bug. It is a surface pattern suggesting a design
problem: worth investigating, not worth fixing on sight. The classic
catalog still pays rent. A long function (CRF001) mixes abstraction
levels and hides the one line you will need. Duplicated blocks
(CRF002) mean a concept exists that nobody named. A switch on one
attribute with three or more branches (CRF003) is a missing type
hierarchy. Magic literals (CRF004) are decisions without owners.
Dead helpers (CRF005) are history nobody deleted. Comments restating
the next line (CRF006) confess that the code cannot speak. Clumped
primitive parameters (CRF007) are a data type trying to be born.
Tests without assertions (CRF008) are documentation wearing a test
costume.

The LLM era added smells the classic catalog never imagined. The
400-character inline prompt is the new magic literal: a carefully
tuned instruction pasted into three call sites, drifting apart with
every edit, untestable because no two copies agree. The fix is the
same as for any literal — one named source of truth — but the
temptation is stronger because prompts feel like prose, not code.
Treat them as code: versioned, reviewed, golden-tested. FACT: DevMate
pins prompt output with `tests/unit/test_prompt_golden.py`, which is
exactly the golden-test treatment an inline prompt never gets.

The helper-module dumping ground is the second new smell: a
`utils.py` or `helpers.py` where every LLM-generated function lands
because no reviewer asked where it belongs. It grows to thousands of
lines, imports everything, and is owned by nobody. The cure is move
method with prejudice: every function earns its module by the data it
touches. A third smell is the confident generated test: dozens of
assertions on mocks of mocks, all passing, none touching behaviour.
Generated tests need the same review as generated code, against the
TQ rules in section 8 and the exercise.

Smells guide, rules decide. A 25-line function with one level of
abstraction and a clear name is fine; a 12-line function with four
nesting levels and two responsibilities is not. Run the audit, read
the finding, then judge. The exercise exists to train exactly this
judgment: twelve mechanical flags, each requiring a human verdict.

### 3. The Catalog, Worked: Eight Moves With Signal, Steps, and Safety

Every move below follows the same contract: name the signal that
triggers it, list the steps in order, and state the safety check that
proves each step. Learn the shape once and all eight become one habit.

**Extract method.** Signal: a fragment with one job, often marked by
a comment paragraph or a block you keep re-reading. Steps: copy the
fragment into a new function with an intent-revealing name, replace
the original with a call, pass what it needs as parameters. Safety:
the suite stays green after each extraction, and the new function is
called from exactly the old site plus any genuine duplicates.

**Inline method.** Signal: a helper whose body no longer earns its
indirection — it only delegates, or its name restates the call.
Steps: replace each call with the body, then delete the method.
Safety: green after every call site is converted; never inline a
method that serves as a test seam, because the seam is the point.

**Extract variable.** Signal: an expression you must parse twice to
understand, especially inside conditions. Steps: assign the
expression to a well-named local, use the name in place. Safety:
green, plus the name states meaning rather than mechanics —
`can_retry` not `flag2`.

**Rename.** Signal: a name that describes storage instead of intent
(`data`, `tmp`, `first`), or a function named after its
implementation instead of its guarantee. Steps: rename the symbol,
let the tooling update references, read every call site once. Safety:
green, plus no reference left behind — the compiler or the suite must
confirm, not your eyes.

**Replace conditional with polymorphism.** Signal: CRF003, three or
more branches testing the same attribute, like the `order.status`
switch in the BAD pack. Steps: define one interface with the branched
operation, create one type per branch carrying its own logic,
replace the switch with a single dispatch call. Safety: pin every
branch output with a golden assertion before touching the switch
(characterization tests from section 5), then move one branch at a
time with green between each.

**Replace magic literals.** Signal: CRF004, a raw value in logic for
the third time — `"pending"` thrice, `0.07` with no name. Steps:
bind the value to one named constant at the right scope, replace
every occurrence, delete the duplicates. Safety: green, plus a search
confirming zero raw occurrences remain. For prompts, the constant
becomes a versioned template with a golden test.

**Introduce parameter object.** Signal: CRF007, the same three
primitives on three or more signatures, like `(customer_id,
currency, precision)` on `price_a`, `price_b`, `price_c`. Steps:
define the grouping type, change one signature and its callers,
repeat per function, then move related behaviour onto the new type.
Safety: green after each signature change; change callers and callee
in the same step so nothing dangles.

**Move method.** Signal: a method reading another object's fields
more than its own — feature envy. Steps: create the method on the
target with the data, delegate from the original, move callers over,
delete the original. Safety: green throughout; the delegation step
keeps both alive so the move is never a leap.

**Decompose conditional.** Signal: a condition spanning lines or a
branch body hiding its own function. Steps: extract the condition,
extract each branch, leaving a three-line if that reads like prose.
Safety: green, plus each extracted name reviewed for honesty —
`is_rollover_window` must mean exactly what it checks.

Two worked pairings show how moves compose. First, the long-function
rescue: extract variable tames the conditions, extract method lifts
each paragraph into a named helper, and move method relocates any
helper that envies another module's data. Three moves, each green,
and a 60-line function becomes five named steps. Second, the status
switch rescue: decompose conditional clarifies the branches,
characterization tests pin each output, replace conditional with
polymorphism distributes the logic, and introduce parameter object
cleans up the constructors the new types now share. Moves chain
because each one ends where the next one's signal begins — learning
to see the signal is the actual skill, and the exercise trains it
with twelve mechanical examples.

### 4. Small-Step Discipline, and When NOT to Refactor

Small steps are the whole safety story. Each step must be reversible
in seconds and verifiable in one gate run: one extraction, one move,
one rename. If a step cannot be reverted cleanly, it was three steps
in disguise — split it. The rhythm is extract, run, commit; move,
run, commit. Boring, fast, and safe beats clever, batched, and
broken. The BAD pack in the exercise is what accumulates when teams
skip this for a year: every rule tripped at once, no single safe
first step visible.

Never mix restructuring with behaviour change. The refactor commit
and the fix commit must be separable, because the day the suite goes
red you need to know which half to blame. Reviewers should be able
to verify a refactoring commit by reading the diff and running the
gate — nothing more.

There are three situations where refactoring is forbidden outright.
First, a red suite: restructuring on red means debugging and
redesigning simultaneously, and you will finish neither. Get green
first, by fix or revert. Second, a live incident: the incident
response changes the minimum to restore service, then the follow-up
adds the regression test, and only then does anyone restructure.
Third, unpinned behaviour: if no test describes what the code does,
writing that characterization test IS the first step, not a prelude
— but until it exists and passes, the code is read-only.

Proportionality governs the rest. A script run twice a year does not
need polymorphism; a billing path touched weekly does. Refactor at
the rate the code is read and changed, heaviest where change is
frequent and failure is expensive. The question is never whether the
code could be cleaner. It is whether the next change will be safer
for this work, now.

### 5. Root Cause Versus Symptom

Most recurring messes persist because every fix treats the symptom.
The symptom is what hurts: brittle tests breaking on each refactor,
the same literal edited in four places, midnight CI failures. The
root cause is the structure that manufactures the hurt: tests
coupled to implementation, unnamed constants, a direct clock read.
Fix the structure once or fix the symptom forever — those are the
only options, and the second one compounds.

The diagnostic habit is five minutes and three questions. What
exactly broke, in the smallest reproducible form? What structure
allowed it — which seam is missing, which concept is unnamed, which
boundary is untested? What is the smallest structural change that
makes this class of failure impossible rather than merely fixed?
The third question is the discriminator. Updating expectations after
each refactor answers the first two; rewriting the tests to assert
observable behaviour answers the third.

Consider the classic: every refactor breaks unrelated tests that
assert private call order. The symptom treatment is adjusting the
expected call sequences again. The root cause is tests asserting
implementation instead of behaviour. The structural fix rewrites
those tests against observable outcomes, after which refactoring
stops breaking them. Same effort as two rounds of expectation
patching, permanent instead of recurring.

Apply the same lens to process. If generated code keeps landing in
the dumping ground, the symptom is the giant module and the cause is
a review checklist with no ownership question. If prompt copies keep
drifting, the cause is the missing template home, not careless
editors. Structures produce behaviour; change the structure.

### 6. The Test Pyramid, With the LLM Twist

The pyramid allocates tests by cost. The bottom is wide: hundreds of
unit tests that run in milliseconds, need nothing but the interpreter,
and fail only when behaviour breaks. The middle is narrower:
integration tests that cross one real boundary each — a database, a
queue, a service — slower and flakier, run deliberately. The top is
thin: end-to-end journeys through the live system, valuable and
expensive, kept to the few paths whose failure would page someone.
Cost, flakiness, and feedback time all grow with height, so volume
belongs at the bottom. An inverted pyramid — a thin unit layer under
a heavy live suite — makes every commit slow and every refactor a
gamble, because the only feedback arrives minutes later and flakes.

FACT: DevMate is built as a pyramid. The bottom is
`projects/04-ai-engineering/devmate/tests/unit/` — files like
`test_chunker.py`, `test_cost.py`, `test_eval_harness.py`, and
`test_api_happy_path.py` run in the default gate with no services.
The middle is `tests/integration/test_services.py`, which needs
Qdrant and Redis running and is excluded from the default run by the
`-m 'not integration and not llm'` addopts. The static base below
even the unit layer is ruff, format, and mypy, which catch entire
defect classes before a single test runs.

The LLM twist reshapes what each layer may assert. The bottom must be
deterministic: chunking, normalization, scoring, cost math, prompt
templates pinned by golden tests. The middle may touch real
retrieval behind the marker. The top holds live quality measurement,
and DevMate implements it as the offline RAGAS gate at
`.github/workflows/ci.yml:71-77` with `--fail-under-hit-at-5 1.0
--fail-under-mrr 0.70`. The iron rule spanning all three layers:
never assert on generated prose in unit tests. Model output varies
between runs and versions, so an exact assertion on it is flaky by
construction — it fails with no code change, which is the definition
in section 10. Assert on everything around the model deterministically,
and measure the model itself statistically at the top.

Newcomers invert the pyramid in two predictable ways. The first is
testing through the model: a unit test that calls the real model to
check chunking end to end, slow and flaky, when a pure function test
would answer in a millisecond. The fix is seam thinking — pass the
chunks in, assert the chunks out, and let the model be someone else's
layer. The second is promoting integration tests into the default
gate: once `test_services.py` runs on every commit without services
present, developers learn that red is normal, and a suite that is
normally red is a suite nobody reads. Keep the default gate instant
and air-gapped; make the service band an explicit, deliberate second
command. FACT: `infra/scripts/local-ci.ps1:37-42` demonstrates the
layering locally, running lint, types, unit tests, and eval as
separate named gates rather than one opaque script.

### 7. Good Tests Assert Behaviour, Shaped as AAA, With One Reason to Fail

A good test proves one behaviour through the public interface and
says nothing about internals. It calls what callers call, feeds
representative inputs, and asserts observable outcomes: return
values, state changes, seam interactions. The moment a test names a
private helper, asserts call order between internals, or patches a
function the module owns, it has stopped testing behaviour and
started testing implementation. Implementation-coupled tests punish
exactly the activity refactoring requires — changing internals —
so they rot into either constant maintenance or a suite everyone
ignores. Both outcomes cost more than the tests ever saved.

The shape that enforces this is Arrange-Act-Assert. Arrange builds
fixtures: inputs, collaborators, frozen time. Act performs the one
action under test — one call, one behaviour. Assert checks the
outcome. Blank lines or comments separate the phases so a failure
points at its phase: arrange failures mean broken fixtures, act
failures mean broken code paths, assert failures mean changed
behaviour. Rule TQ001 flags tests with no visible separation, and
the exercise GOOD twins carry `# arrange`, `# act`, `# assert`
markers to show the shape explicitly.

One reason to fail completes the contract. Each test diagnoses
exactly one broken behaviour, so a red test names its culprit. The
BAD `test_total_combined` asserts pricing, discount, and receipt in
one body — three reasons to fail, and a failure explains nothing
without archaeology. Split it three ways and each failure is a
diagnosis. As a corollary, prefer one behaviour per test and few
assertions per behaviour: multiple assertions on the same outcome
are fine, assertions on three outcomes are three tests sharing a
name.

Behaviour-first also decides what not to test. Generated
configuration, trivial delegation, and framework mechanics earn no
tests; they earn deletion or trust in the framework's own suite.
Test the decisions your team made: the rounding rule, the retry
budget, the chunk boundary. Everything else is coverage theatre.

### 8. Doubles: Stubs, Mocks, Spies, Fakes — and the Seam They Stand On

A test double stands in for a dependency so the unit runs isolated:
fast, deterministic, and diagnostic. There are four kinds and they
differ in what they verify. A stub answers with canned data and
verifies nothing — the rate table that always returns `1.08`. A mock
answers and additionally verifies the interaction happened: called
once, with these arguments. A spy records calls for assertions
written after the act phase, useful when the interesting evidence is
a sequence rather than a single call. A fake is a working lightweight
implementation, like an in-memory queue standing in for the real
broker when the contract matters but the infrastructure is too
heavy. Choose the weakest double that suffices: stub over mock, mock
over fake, nothing over stub.

None of this works without a seam: a place where behaviour can be
substituted without editing the unit. Constructor parameters,
imported clients passed in, a clock argument — these are seams.
Hard-coded imports, direct system calls, and module-level singletons
are concrete: no seam, no isolation, and the test must use the real
thing with all its cost and flakiness. Designing for testability
means designing seams at every outside-world boundary: network,
clock, disk, randomness. Pure logic needs no seams and no doubles,
which is why pushing logic away from boundaries makes everything
cheaper to test.

Mock at the seam is the placement rule, and rule TQ004 enforces it.
Patching `billing.price_a` — a pure internal helper the module owns
— couples the test to implementation and hides the real behaviour
behind a lie the test itself wrote. Patch the HTTP client, the clock,
the store: the edges where the unit meets a world you do not
control. A useful review heuristic: if removing the mock makes the
test pass trivially or fail meaninglessly, the mock was load-bearing
and the test proved nothing. Mocks should remove accident — latency,
cost, flakiness — never remove the behaviour under test.

Over-mocking has its own smell: tests that assert elaborate call
choreography between internals while the observable outcome goes
unchecked. When the suite is green but nobody believes it, count the
mocks per test. More than one mock is a design hint that the unit is
too big or the seam is in the wrong place.

A worked seam design shows the full ladder. Start with the untestable
version: `send_receipt(order)` reads the clock, fetches rates over
HTTP, and writes to disk, all through hard-coded calls. Step one:
take the rates client as a parameter — the network seam appears and
a stub covers pricing. Step two: take the clock as a parameter — the
time seam appears and frozen instants cover expiry. Step three: return
the receipt instead of writing it — the disk seam disappears because
there is no more side effect to isolate. What remains is pure logic
with no doubles at all, tested by plain assertions. The lesson: every
seam you remove by pushing side effects outward is a mock you never
write, and the cheapest double is the one the design made unnecessary.

### 9. Property-Based Tests, Mutation Tests, and Coverage as a Floor

Three techniques answer three different questions about a suite.
Property-based testing asks whether invariants hold across inputs:
generate hundreds of cases and assert what must always be true.
Round-trips (chunk then rejoin equals the original), bounds
(discounts never drive totals negative), idempotence (formatting
twice equals formatting once) — properties catch the edge case no
human would hand-write, like empty inputs, unicode boundaries, and
maximal lengths. Use properties where the invariant is clearer than
any example, and keep example tests where the specific case
documents intent.

Mutation testing asks whether the suite would catch real bugs: seed
small defects — flipped operators, skipped calls, shifted constants —
and require failures. Each seeded defect is a mutant; the kill rate
is the share the suite catches. A suite can be entirely green over
entirely broken code if its assertions are weak, and only mutation
reveals that. Run it on the critical paths — billing math, retry
budgets, auth checks — not necessarily on everything, because mutants
cost compute. When the kill rate is low, the prescription is
stronger assertions on existing tests, not more tests with the same
weak assertions.

Coverage asks only what ran. It is a floor, never a proof: below the
bar, something is definitely untested; above it, nothing is proven
about assertion strength. FACT: DevMate reports coverage with
`--cov=devmate` in `ci.yml:65` but gates quality separately through
the eval thresholds at `:71-77` — measurement and judgment kept
apart, exactly the right relationship. Use coverage to find the
untested module, the unexercised branch, the dead code that CRF005
should have caught. Never use it to argue a suite is good. A suite
with 95 percent coverage and a 50 percent kill rate is a decorated
blind spot.

Together the three form a ladder. Coverage finds what never runs.
Properties probe what examples miss. Mutation judges whether any of
it would catch a bug. Climb in order, and stop climbing when the next
rung costs more than the defects it would find — proportionality
applies to testing effort too.

### 10. The LLM Pyramid in Practice, Flaky Causes, and TDD's Honest Role

Put the previous sections to work on a realistic pipeline: chunking,
normalization, scoring, prompt assembly, model call, answer
rendering. The deterministic unit layer covers everything up to the
model boundary: chunkers with fixed documents, normalizers with
tricky unicode, scorers with hand-computed expectations, prompt
templates with golden fixtures. FACT: this mirrors DevMate's unit
directory — `test_chunker.py` for the chunking layer, `test_cost.py`
for budget math, `test_prompt_golden.py` for template output,
`test_eval_harness.py` for the measurement code itself. None of these
needs a key, a service, or luck, and all run in the default gate.

The integration band behind the marker covers retrieval against real
services: Qdrant up, Redis up, documents ingested, assertions on
ranked results rather than prose. FACT:
`tests/integration/test_services.py` is precisely this band, excluded
from the default addopts and run deliberately with services alive.
The thin live top measures answer quality statistically — hit rates
and reciprocal ranks with thresholds, rerun-tolerant — never exact
prose equality. New model version, same thresholds, no test edits:
that stability is how you know the layers are correctly assigned.

Flakiness has four causes and each has one fix at a seam. Time:
inject or freeze the clock instead of reading it. Randomness: seed
it or move it behind a parameter the test controls. Ordering:
isolate state per test so execution order cannot matter. Shared
state: build fresh fixtures instead of reusing module-level data.
When a test flakes, classify first into one of the four, then fix
the seam — never wrap the suite in retries, which converts
diagnosable flakes into mysterious slowness.

TDD's honest role in this picture is design feedback, not coverage
generation. Writing the failing test first forces the seam, the
name, and the observable outcome to exist before the implementation
seduces you into testing internals. It is worth it on tricky logic
with unclear interfaces and unnecessary on obvious glue. Red, green,
refactor remains the loop, but the refactor step is only safe
because the first two steps produced a test that asserts behaviour.
Used honestly, TDD front-loads every lesson of this lecture into
the smallest possible cycle.

Know also what TDD does not do, so expectations stay honest. It does
not design the system: interfaces still need the thinking from the
contracts and domain-modeling material, and a test-first muddle is
still a muddle. It does not replace the pyramid: test-first unit
tests still need the integration band and the statistical top, or
confidence stops at the module edge. And it does not work on red or
in incidents — the discipline of section 4 outranks enthusiasm in
every emergency. TDD is one loop inside the larger practice this
lecture teaches: green-gated, seam-placed, behaviour-asserted
engineering, repeated until the codebase trusts its own tests.

---

## Common Mistakes to Avoid

1. ❌ Mixing a behaviour fix into a refactoring commit. ✅ Keep
   restructuring and fixes in separable commits with green between.
2. ❌ Restructuring while the suite is red. ✅ Fix or revert to
   green first; red forbids refactoring entirely.
3. ❌ Pasting a 400-character prompt into three call sites. ✅ Keep
   one versioned template with a golden test behind it.
4. ❌ Asserting exact model prose in a unit test. ✅ Assert
   deterministic layers exactly; measure prose statistically at top.
5. ❌ Mocking internal helpers the module owns. ✅ Place doubles at
   the seam: network, clock, disk, randomness.
6. ❌ Treating 95 percent coverage as proof of a good suite. ✅ Hold
   coverage as a floor and check assertion strength by mutation.
7. ❌ Patching brittle expectations after every refactor. ✅ Rewrite
   the tests to assert observable behaviour — fix the cause.
8. ❌ Wrapping a flaky suite in retries. ✅ Classify the flake into
   time, randomness, ordering, or shared state and fix the seam.

---

## Best Practices

1. Get green before the first structural edit, and stay green after each step.
2. Keep every refactoring step reversible in seconds and verifiable in one gate run.
3. Name the concept before duplicating the code: extract on the second copy, never the fourth.
4. Pin branch outputs with golden assertions before replacing a conditional with polymorphism.
5. Bind every repeated literal once at the right scope; prompts become versioned templates.
6. Group travelling parameters into a named type at three signatures, not ten.
7. Move envied methods to the data they use; delegate, migrate callers, then delete.
8. Write tests against observable behaviour through the public interface, never internals.
9. Shape every test as Arrange-Act-Assert with visible phase separation.
10. Give each test one reason to fail; split multi-subject tests until failures diagnose themselves.
11. Mock only at outside-world seams, choosing the weakest double that suffices.
12. Cover deterministic layers exactly, integration behind markers, live quality statistically.
13. Use coverage to find untested code, properties to probe invariants, mutation to judge strength.
14. Classify every flake into time, randomness, ordering, or shared state, then fix the seam.

---

## Practice Exercises

1. Run the track exercise and read all 19 BAD findings; for each,
   write the one-sentence structural verdict a reviewer would leave.
2. Take the BAD `calculate_total` and apply extract method twice with
   a gate run between, keeping every intermediate step green.
3. Rewrite `test_total_combined` as three AAA tests with one subject
   each, then confirm TQ001, TQ002, and TQ003 stay silent.
4. Convert the `order.status` switch to dispatched types behind one
   interface, pinning each branch with a golden assertion first.
5. Add a property test for the GOOD `money` helper (currency label
   preserved for any amount) and one mutant the suite must kill.

---

## Summary

1. Refactoring is behaviour-preserving restructuring, proven safe by a green suite.
2. Smells hint at design problems; LLM-era smells include inline prompts and dumping grounds.
3. Eight catalog moves cover most restructuring; each has a signal, steps, and a safety check.
4. Small reversible steps with green between are the entire safety story.
5. Red suites, live incidents, and unpinned behaviour forbid refactoring outright.
6. Fix root causes — missing seams, unnamed concepts — not recurring symptoms.
7. The pyramid puts volume at the cheap deterministic bottom and keeps the live top thin.
8. Good tests assert observable behaviour in AAA shape with one reason to fail.
9. Doubles belong at outside-world seams; mocking internals couples tests to implementation.
10. Coverage is a floor, properties probe invariants, and mutation judges assertion strength.

**Next lecture:** Lecture 02 will take the seams and doubles from
sections 8 and 10 into the integration band: service-backed tests,
contract tests at bounded-context edges, and the reliability patterns
whose timeouts and retries need a live pyramid top to prove them.

*AI Engineer Lab — System Design track, software-craftsmanship lane.*
