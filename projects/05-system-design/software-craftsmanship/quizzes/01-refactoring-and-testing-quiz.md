# Quiz 01: Refactoring and Testing

Test your grasp of Lecture 01: refactoring discipline, smells, the
catalog moves, the test pyramid, good-test habits, doubles, and
property-based and mutation testing. 15 questions, 4 options each.

**Scoring:** Easy = 1 point, Medium = 2 points, Hard = 3 points.
Maximum: 5x1 + 7x2 + 3x3 = 28 points.

---

## Questions

### 1. What makes a change a refactoring?

**Difficulty:** Easy

A. Any edit that improves the code
B. A behaviour-preserving restructuring done under a green suite
C. A rewrite of the module in a cleaner style
D. A performance optimization with benchmarks

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Refactoring changes internal structure without changing
observable behaviour, and the green suite is the evidence. A says
nothing about behaviour; C is a rewrite, not a refactoring; D changes
performance characteristics deliberately.
</details>

---

### 2. When is it acceptable to refactor?

**Difficulty:** Easy

A. Only during a dedicated cleanup sprint
B. Whenever the suite is green and the step is small and reversible
C. Only when a file exceeds 500 lines
D. Whenever the code looks old

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Refactoring is continuous hygiene gated by a green
suite and small steps, not a calendar event. A defers it until the
mess is expensive; C and D are not safety conditions.
</details>

---

### 3. Which layer belongs at the wide bottom of the test pyramid?

**Difficulty:** Easy

A. End-to-end tests against live services
B. Manual release checklists
C. Fast deterministic unit tests with no network
D. Load tests

<details><summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** The bottom is wide because unit tests are cheap, fast,
and deterministic — DevMate's `tests/unit/` runs in the default gate
while `tests/integration/test_services.py` needs live services. A, B,
and D are slow or manual and belong at the thin top or outside the gate.
</details>

---

### 4. What does Arrange-Act-Assert give a test?

**Difficulty:** Easy

A. Three assertions per test
B. A visible setup, single action, and expectation structure
C. A way to test three functions at once
D. Automatic mock generation

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** AAA separates fixture setup from the one behaviour
under test and its expectations, so a failure points at one cause.
A and C describe the multi-assert, multi-subject habits TQ002 and
TQ003 flag; D is unrelated.
</details>

---

### 5. A test fails only when one behaviour breaks. What is this?

**Difficulty:** Easy

A. One reason to fail
B. 100 percent coverage
C. Mutation adequacy
D. Flakiness

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** One reason to fail means the test asserts a single
behaviour, so the failure diagnoses itself. B measures execution, not
diagnosis; C measures suite strength; D is non-determinism.
</details>

---

### 6. A 400-character prompt is inlined in three call sites. What is the first move?

**Difficulty:** Medium

A. Extract it to a named constant or template and replace the literals
B. Add a comment above each copy explaining the prompt
C. Mock the language model in all three tests
D. Increase coverage thresholds

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** This is the replace-magic-literals move: one named
source of truth, then the three sites reference it. B (CRF006) restates
instead of fixing; C tests around the duplication; D measures it.
</details>

---

### 7. Three functions each take `(customer_id, currency, precision)`. Which rule fires and what fixes it?

**Difficulty:** Medium

A. CRF004 — inline the parameters
B. CRF007 — introduce a parameter object grouping the trio
C. CRF002 — delete two of the functions
D. TQ003 — merge the three tests

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The same three primitive parameters across three or
more signatures (CRF007) signal a missing concept; a parameter object
names it and shortens every signature. A misfires the wrong rule;
C destroys behaviour; D answers a different layer.
</details>

---

### 8. A test patches `billing.calculate_total` (a pure internal helper). What is wrong?

**Difficulty:** Medium

A. Nothing — all helpers should be mocked
B. TQ004 — the mock sits inside the module instead of at the boundary seam
C. TQ002 — the test has no assertions
D. CRF005 — the helper is dead code

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Mocks belong at the seam where the unit meets the
outside world (network, clock, disk), not on internal helpers you own.
Mocking internals couples the test to implementation and hides the real
behaviour. A states the over-mocking anti-pattern; C and D are
different rules.
</details>

---

### 9. What is the difference between a stub and a mock?

**Difficulty:** Medium

A. There is none — the terms are interchangeable
B. A stub supplies canned answers; a mock also verifies interactions happened
C. A stub verifies calls; a mock supplies answers
D. Stubs are for databases, mocks are for networks

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** A stub answers with fixed data so the test can run; a
mock additionally records and asserts the interaction (called once, with
these args). C swaps the definitions; A and D are false.
</details>

---

### 10. Coverage is at 95 percent but mutation testing kills only half the mutants. What does this mean?

**Difficulty:** Medium

A. The suite executes code without really checking it — coverage is a floor, not a proof
B. The coverage tool is misconfigured
C. More end-to-end tests are needed
D. The mutants are invalid and should be ignored

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** Coverage records which lines ran; mutation testing
checks whether the assertions would catch wrong code. High coverage
with a low kill rate means weak assertions. B blames the tool; C adds
slow tests instead of stronger unit assertions; D dismisses the signal.
</details>

---

### 11. Why must unit tests never assert on generated prose?

**Difficulty:** Medium

A. String comparison is too slow for unit tests
B. Model output is non-deterministic, so the assertion is flaky by construction
C. Prose cannot be stored in fixtures
D. Linters forbid long string literals

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Generated text varies between runs and model versions,
so an exact assertion on it fails without any code change — the
definition of flaky. Deterministic layers (chunking, normalization,
scoring, golden prompts like `test_prompt_golden.py`) carry the unit
assertions instead. A is false; C is false; D is false.
</details>

---

### 12. A test fails only on midnight CI runs. What is the most likely cause class?

**Difficulty:** Medium

A. Shared mutable state between tests
B. A wall-clock dependency — time is an unmocked seam
C. Wrong assertion style
D. Missing type annotations

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Time-dependent failures (midnight rollover, dates,
timeouts) point at the clock seam: the code reads real time instead of
an injected clock or frozen value. A causes order-dependence, not
clock-dependence; C and D do not cause time-correlated flakes.
</details>

---

### 13. A chain of four `elif` branches switches on `order.status`. Which refactoring applies, and what is the safety precondition?

**Difficulty:** Hard

A. Inline method; precondition is high coverage
B. Replace conditional with polymorphism; precondition is a green suite plus one small step at a time
C. Extract variable; precondition is reviewer approval
D. Decompose conditional; precondition is deleting the tests first

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** A multi-branch switch on one attribute (CRF003) is the
 textbook signal for polymorphism: each branch becomes a type or
strategy behind one interface. Safety comes from the green suite and
small steps (extract, then move, re-running each time). A names the
wrong move; C is too weak for four branches; D inverts safety.
</details>

---

### 14. Your suite is green, but every refactor breaks unrelated tests that assert private call order. What is the root problem?

**Difficulty:** Hard

A. The tests assert implementation instead of behaviour — treat the cause (rewrite to observable outcomes), not the symptom (updating expectations each time)
B. Refactoring is unsafe and should stop
C. Coverage is too low
D. The tests need more mocks

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** This is root cause versus symptom: brittle tests that
lock internal call order break on any restructuring. Patching
expectations after each refactor treats the symptom; rewriting the
tests to assert observable behaviour removes the cause. B abandons the
practice; C misdiagnoses; D deepens the coupling.
</details>

---

### 15. Design the deterministic test strategy for a chunking + scoring + LLM-answer pipeline. Which split is correct?

**Difficulty:** Hard

A. Assert exact LLM prose in unit tests; keep one integration test
B. Unit-test chunking, normalization, and scoring deterministically; gate prompts with golden cases like `test_prompt_golden.py`; hold live retrieval behind the `integration` marker and the offline eval gate
C. Skip unit tests; run everything live end-to-end
D. Mock chunking and scoring; assert only on the LLM call

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** This is the LLM pyramid in practice: a wide
deterministic bottom (pure functions, golden prompts), a marked
integration band needing services (`tests/integration/test_services.py`,
excluded from the default addopts), and a thin live top (offline RAGAS
gate at `--fail-under-hit-at-5 1.0 --fail-under-mrr 0.70`). A asserts
flaky prose; C inverts the pyramid; D mocks the parts you own and
asserts on the part you do not.
</details>

---

## Score Tracking

| # | Topic | Difficulty | Points | Your score |
|---|-------|------------|--------|------------|
| 1 | Refactoring defined | Easy | 1 | |
| 2 | When to refactor | Easy | 1 | |
| 3 | Pyramid bottom | Easy | 1 | |
| 4 | AAA structure | Easy | 1 | |
| 5 | One reason to fail | Easy | 1 | |
| 6 | Magic literals | Medium | 2 | |
| 7 | Parameter object | Medium | 2 | |
| 8 | Mock at the seam | Medium | 2 | |
| 9 | Stub vs mock | Medium | 2 | |
| 10 | Mutation vs coverage | Medium | 2 | |
| 11 | No prose asserts | Medium | 2 | |
| 12 | Clock seam flake | Medium | 2 | |
| 13 | Conditional to polymorphism | Hard | 3 | |
| 14 | Root cause vs symptom | Hard | 3 | |
| 15 | LLM pyramid strategy | Hard | 3 | |
| | **Total** | | **28** | |

**Interpretation:** 24-28 expert — you can lead a refactoring safely;
18-23 proficient — review the missed explanations; 10-17 developing —
re-read the lecture Key Concepts; below 10 — restart from the pyramid
and AAA sections.

## Answer Key

| # | Answer | Rule / Concept |
|---|--------|----------------|
| 1 | B | Refactoring defined |
| 2 | B | Small-step discipline |
| 3 | C | Test pyramid |
| 4 | B | AAA |
| 5 | A | One reason to fail |
| 6 | A | Replace magic literals (CRF004) |
| 7 | B | Parameter object (CRF007) |
| 8 | B | Mock at the seam (TQ004) |
| 9 | B | Doubles |
| 10 | A | Coverage as floor |
| 11 | B | Deterministic unit layer |
| 12 | B | Flaky causes: time |
| 13 | B | Replace conditional (CRF003) |
| 14 | A | Root cause vs symptom |
| 15 | B | LLM pyramid in practice |

*AI Engineer Lab — System Design track, software-craftsmanship lane.*
