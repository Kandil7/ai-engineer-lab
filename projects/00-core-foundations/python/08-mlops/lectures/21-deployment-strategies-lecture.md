# MLOps — 21: Deployment Strategies

## Topic Overview

A validated model still has to reach production traffic safely. How it
gets there
— all at once, a slice at a time, side-by-side, or behind a switch — is
the
deployment strategy, and the choice decides the blast radius of a bad
release.
Four patterns cover the space: **shadow** (score without serving),
**canary** (a
live slice), **blue-green** (two environments, one switch), and **A/B**
(a
statistical comparison). Lecture 12 taught promotion and canary; Lecture
14
taught A/B testing; this unit unifies them, adds blue-green, and gives
the
decision framework that chooses among them.

The three questions that decide the strategy are risk, reversibility,
and cost.
How much damage does a bad release do (risk)? How fast can you undo it
(reversibility)? How much does running two versions cost (two
environments, split
traffic)? A low-risk internal tool ships directly; a high-risk payment
model
goes shadow, then canary, then full — and blue-green is the answer when
instant,
total rollback is worth the price of two environments.

Rollback is not a nice-to-have; it is a deployment property. Every
strategy here
is judged first on how it fails — because the strategy you chose is the
one you
live with at 2 a.m. when the metrics turn red.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the deployment problem: risk, reversibility, observability
2. Describe shadow deployment and what it validates without serving
3. Describe canary deployment and the slice-and-monitor loop
4. Describe blue-green deployment and the instant-switch property
5. Explain A/B testing as a deployment strategy, not just an experiment
6. Implement rollback as a first-class deployment operation
7. Choose a strategy by risk, traffic, cost, and reversibility

## Prerequisites

| Need | Where |
|---|---|
| CI promotion and canary | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |
| A/B testing and statistics | `08-mlops/lectures/14-ab-testing-models-lecture.md` |
| Monitoring and alerts | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |
| Model registry stages | `08-mlops/lectures/04-model-registry-lecture.md` |

## 1. The Deployment Problem

Shipping a model is moving validated code and weights into live traffic.
Three
properties decide how safely that happens:

- **Risk**: how much damage a bad release does (internal tool vs payment model).
- **Reversibility**: how fast and completely you can undo it.
- **Observability**: whether you can tell, in minutes, that it is bad.

```python
deployment = {
    "candidate": "credit_risk v3.2.0",
    "risk": "high",  # decides about people and money
    "reversibility": "minutes",  # must be able to undo fast
    "observability": "p95 + error rate + fairness",  # watched from minute one
}
```

A strategy is a point in this space. Direct deploy maximizes speed and
minimizes
cost — and maximizes risk. The other three trade cost for safety in
different
ways.

## 2. Shadow Deployment

### Score without serving

A shadow deployment runs the candidate on live traffic **without serving
it**:
real requests are scored by both champion and candidate, and the outputs
are
compared offline. Users never see the candidate's answers, so a bad
candidate
does zero harm.

```python
def shadow_compare(candidate_scores, champion_scores, tolerance):
    """Compare a shadow candidate to the champion on identical live inputs."""
    diffs = [abs(c - h) for c, h in zip(candidate_scores, champion_scores)]
    mean_diff = sum(diffs) / len(diffs)
    return mean_diff <= tolerance, mean_diff
```

### What it validates

Shadow validates the candidate on the *real* input distribution — which
the
frozen eval set approximates but never equals. It catches train/serve
skew,
unexpected input shapes, and latency under real load, all with zero user
impact.

### What it cannot do

Shadow cannot measure *user* impact: engagement, conversion, or
satisfaction.
Only serving the candidate (canary, A/B) reveals how users respond.
Shadow is
the safety check, not the final verdict.

## 3. Canary Deployment

### A slice of live traffic

A canary routes a small fraction (say 5%) of live requests to the
candidate and
watches its metrics — latency, error rate, accuracy proxy, fairness —
against
the champion's for a window. If the canary passes, the slice grows; if
it fails,
the slice closes and the candidate rolls back.

```python
def canary_decision(candidate_metric, champion_metric, threshold, higher_better=True):
    if higher_better:
        passed = candidate_metric >= champion_metric - threshold
    else:
        passed = candidate_metric <= champion_metric + threshold
    return ("expand" if passed else "rollback"), passed
```

### The loop

Canary is a loop, not a step: 5% → 25% → 50% → 100%, with a gate at each
expansion. Each gate is the same comparison — candidate versus champion
within
tolerance — applied to progressively more traffic. The gradual expansion
bounds
the blast radius at every moment.

## 4. Blue-Green Deployment

### Two environments, one switch

Blue-green keeps **two identical production environments**. Blue serves
live
traffic; green runs the candidate. When green passes validation, the
router
switches all traffic from blue to green in one step. If green
misbehaves, the
router switches back — instantly, totally.

```python
def blue_green_switch(current, candidate, health_ok):
    """Switch traffic only on health; rollback is the same operation in reverse."""
    if health_ok:
        return candidate, f"switched {current} -> {candidate}"
    return current, f"holding on {current}: candidate unhealthy"
```

### Why it is different

Blue-green is the only strategy with **instant, total rollback**: one
router
change reverts 100% of traffic. Canary rolls back a slice; blue-green
rolls back
everything. That property is worth the price of a second environment
when the
cost of a bad release exceeds the cost of idle capacity.

### The cost

Two environments cost twice the serving capacity during the switch
window. For
expensive GPU serving, that is real money — which is why blue-green is
reserved
for high-risk releases where reversibility is worth it.

## 5. A/B Testing as Deployment

### The statistical comparison

An A/B test splits traffic between champion and candidate and compares a
*business* metric (conversion, engagement, revenue) with statistical rigor —
sample size, significance, guardrails (Lecture 14). It answers the
question the
other strategies cannot: not "is the candidate safe" but "is it better
for the
business."

```python
def ab_decision(lift, p_value, alpha=0.05, guardrails_ok=True):
    if not guardrails_ok:
        return "rollback: guardrail violated"
    if p_value < alpha and lift > 0:
        return "promote: significant positive lift"
    return "hold: no significant lift"
```

### Deployment, not just experiment

A/B is a deployment strategy when the *winner* becomes the new default —
the test
is the promotion path. The statistical machinery (Lecture 14) is the
gate, and
the traffic split is the rollout. This is how product-facing ML ships:
measured,
not hoped.

## 6. Rollback

### The first-class operation

Rollback is not "undo the deploy by hand"; it is a tested, one-step
operation
that restores a prior version with its config and data reference. Every
strategy
above must answer: how do I get back, and how fast?

```python
def rollback(deployments, target_version):
    """Restore a prior version; the registry knows every version's artifact."""
    if target_version not in deployments:
        return None, f"FAIL: {target_version} unknown, cannot roll back"
    return target_version, f"rolled back to {target_version}"
```

### The reversibility ranking

From least to most reversible: direct deploy (manual, slow), canary
(close the
slice), A/B (stop the test), blue-green (one router switch, instant and
total).
Risk and reversibility are the two axes of every deployment choice.

## 7. The Decision Framework

### The table

| Strategy | User impact if bad | Reversibility | Cost | Best for |
|---|---|---|---|---|
| Shadow | none | n/a (never served) | +1 scoring copy | validating on real inputs |
| Canary | bounded (the slice) | close the slice | split traffic | gradual, observed rollout |
| Blue-green | all-or-nothing | instant, total | two environments | high-risk, fast rollback |
| A/B | split | stop the test | split traffic + stats | proving business lift |
| Direct | total | manual | cheapest | low-risk internal tools |

### The questions

1. **What is the risk?** High risk rules out direct deploy.
2. **Must rollback be instant?** Yes → blue-green. Gradual is fine → canary.
3. **Do you need real-input validation first?** Shadow before any serving.
4. **Do you need to prove business lift?** A/B with statistics.
5. **What can you afford?** Two environments cost; shadow/canary are cheaper.

```python
def choose_strategy(risk, need_instant_rollback, need_business_proof, budget_for_two_envs):
    if risk == "low":
        return "direct"
    if need_business_proof:
        return "A/B"
    if need_instant_rollback and budget_for_two_envs:
        return "blue-green"
    return "shadow, then canary"
```

## 8. Feature Flags and Kill Switches

### Decouple deploy from release

A feature flag separates *shipping code* from *enabling it*. The new
model deploys
dark (present but inactive), and the flag turns it on for a slice, a
segment, or
everyone — without another deploy. This turns every strategy above into
a runtime
decision rather than a deployment event.

```python
# The flag is the switch; the strategy is the policy behind it.
if flags.enabled("model_v32", user_id=user_id, rollout=0.05):
    return candidate.predict(x)
return champion.predict(x)
```

### The kill switch

A kill switch is a flag whose only job is instant disable: one change
reverts
100% of traffic to the champion, no deploy, no router change. It is the fastest
possible rollback, and every high-risk model should have one.

### The combination

Flags compose with strategies: a canary *is* a flag at 5%; blue-green
*is* a flag
that flips the router; A/B *is* a flag split by experiment. The flag is
the
mechanism, the strategy is the policy — and implementing both as flags
keeps the
mechanism uniform.

### Flag hygiene

Stale flags are technical debt: a codebase with 200 dead flags is
unmaintainable.
Remove a flag once its rollout is complete (the winner is the only
path). Flag
hygiene is part of the deployment discipline, not an afterthought.

## 9. Post-Deploy Validation

### Smoke tests after promotion

Promotion is not the end; the deployed service is smoke-tested
immediately — a
minimal check that it responds correctly to known inputs. This is the CI
smoke
test (Lecture 12) run against the live endpoint, catching packaging and
environment errors that only appear in production.

### The validation window

The first N minutes after a release get heightened alerts: error rate,
latency,
business metric, and fairness are watched at a lower threshold than
steady state.
A breach in the window triggers automatic rollback, because a
release-time
regression is the most likely failure.

### What to watch

The same four families as section 7 of Lecture 19: accuracy (or a
proxy),
latency p95, error rate, and resource utilization. The post-deploy
window watches
them all, and the dashboard shows the new version's lines against the
old one's.

### The rollback trigger

Automatic rollback fires when a validation check fails inside the window
— no
human needed. The trigger condition and the rollback action are both
tested in
staging, so the 2 a.m. incident is a drill that has already been run.

## Every Use Case

- **Every model release**: a deployment strategy is named, never "just ship it".
- **High-risk models**: shadow, then canary, then full — the safest sequence.
- **Regulated releases**: the strategy and its evidence are part of the audit.
- **Product ML**: A/B proves lift before the winner becomes the default.
- **Internal tools**: direct deploy is fine when risk is genuinely low.
- **Incident response**: rollback is the first action, and it is tested.
- **Cost reviews**: the two-environment cost of blue-green is justified explicitly.

## Real-World Use Cases for AI Engineers

- **Payments engineer**: blue-green for a fraud model, because a bad release
  costs money every minute and instant rollback is worth the second environment.
- **Recommendations engineer**: shadow first (validate on real traffic), then a
  canary slice, then an A/B to prove engagement lift — the full sequence.
- **Internal-tools engineer**: direct deploy for a log-parsing model with five
  users; the risk does not justify the ceremony.
- **Platform engineer**: deployment strategies are templates (shadow/canary/
  blue-green/A-B) teams select by risk, with rollback tested in staging first.
- **RAG service (DevMate)**: a canary on the new retriever with recall@k as the
  comparison metric, expanding only while the canary matches the champion.

## Common Mistakes to Avoid

### Mistake 1: Direct deploy of a high-risk model
Maximum blast radius for minimum ceremony. Match the strategy to the
risk.

### Mistake 2: No rollback plan
A strategy without a tested rollback is not a strategy. Test the undo in
staging.

### Mistake 3: Canary without a decision rule
A 5% slice with no gate is just a slow direct deploy. Define pass/fail
before it ships.

### Mistake 4: Shadow confused with serving
Shadow validates inputs, not user impact. It is a safety check, not a
verdict.

### Mistake 5: A/B without guardrails
A lift in the target metric that breaks a guardrail (fairness, latency)
is a
failure, not a win.

### Mistake 6: Blue-green for every release
Two environments for a low-risk model is waste. Reserve blue-green for
high risk.

### Mistake 7: Unmeasured rollback time
"Minutes" that are actually hours in an incident. Measure the rollback
drill.

## Best Practices

1. Name the deployment strategy for every release; never "just ship it"
2. Start high-risk releases with shadow, then canary, then full
3. Define the canary pass/fail rule before the slice goes live
4. Test rollback in staging; measure how long it takes
5. Require guardrails alongside A/B lift (accuracy, fairness, latency)
6. Record the strategy and its evidence in the registry version
7. Match the strategy to risk, not to habit
8. Keep the previous version warm until the new one is proven
9. Alert on the comparison metrics from minute one of any serving
10. Price the two-environment cost explicitly when choosing blue-green

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Shadow scoring | +1 scoring copy | O(traffic) | sample the traffic |
| Canary slice | per-window | split traffic | smaller slice, longer window |
| Blue-green | switch window | 2x environments | canary (gradual, cheaper) |
| A/B test | until significance | split + stats | canary (no statistics) |
| Rollback | seconds-minutes | prior version warm | — (non-negotiable) |

## AI Engineering Relevance

**Where this shows up:** every production release. Deployment strategy is the
answer to "how does a good model reach users without a bad release
hurting
them."

| Concept here | Used for |
|---|---|
| Shadow | Zero-risk validation on real inputs |
| Canary | Bounded, observed rollout |
| Blue-green | Instant, total rollback |
| A/B | Proving business lift |
| Rollback | The reversibility every strategy must have |

**Scale note:** at one model the strategy is a runbook; at fifty it is a set of
templates teams pick by risk. The router, the comparison metrics, and
the tested
rollback are the shared infrastructure that makes every team's release
safe.

## Practice Exercises

### Exercise 1: Shadow Comparison (Easy)
Implement `shadow_compare(candidate_scores, champion_scores, tolerance)`
and
test the pass/fail cases.

### Exercise 2: Canary Decision (Medium)
Implement `canary_decision(candidate_metric, champion_metric,
threshold)` for
higher-better and lower-better metrics.

### Exercise 3: Blue-Green Switch (Medium)
Implement `blue_green_switch(current, candidate, health_ok)` and test
the
switch, hold, and rollback-by-reverse cases.

### Exercise 4: Strategy Choice (Hard)
Implement `choose_strategy(risk, need_instant_rollback,
need_business_proof,
budget_for_two_envs)` covering all five outcomes; write the decision
table as
tests.

## Summary

| Concept | Description |
|---|---|
| Shadow | Score live traffic without serving it |
| Canary | A live slice, gated at each expansion |
| Blue-green | Two environments, one instant switch |
| A/B | A statistical comparison that decides promotion |
| Rollback | The tested, first-class undo every strategy must have |

A deployment strategy is a point in risk/reversibility/cost space.
Shadow
validates, canary bounds, blue-green reverts instantly, and A/B proves
lift.
Choose by risk, test the rollback, and record the choice — because the
strategy
you pick is the one you live with at 2 a.m.

## Quick Reference

| Task | Idiom |
|---|---|
| Zero-risk check | shadow on live traffic, compare offline |
| Bounded rollout | canary slice with a gate per expansion |
| Instant rollback | blue-green: one router switch |
| Prove lift | A/B with significance + guardrails |
| Undo | tested rollback to a warm prior version |
| Choose | risk → reversibility → cost, in that order |

## Next Steps

Next: **[16 Case Study E2E](16-case-study-e2e-lecture.md)** — the full
lifecycle
that composes every unit in this module.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://martinfowler.com/bliki/CanaryRelease.html


