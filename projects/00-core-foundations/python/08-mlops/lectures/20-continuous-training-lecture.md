# MLOps — 20: Continuous Training

## Topic Overview

Models degrade. The data shifts, the world changes, and a model that
scored 0.91
at launch scores 0.84 six months later — silently, unless someone is
watching.
Continuous training (CT) is the automation that rebuilds the model on a
signal
rather than on a calendar: drift crosses a threshold, performance drops,
enough
new data arrives, and the retraining pipeline runs itself — train,
evaluate,
compare against the champion, and promote only if the challenger wins.

CT is the "continuous" half of CI/CD for ML that most teams skip. CI
validates a
*code* change; CT validates a *time* change — the same gates, but triggered by
the data's behavior rather than a commit. Without it, every model has an
expiration date that no one tracks. With it, the model is a living
system that
refreshes itself inside guardrails.

The two failure modes define the discipline. **Stale** (never
retraining) lets
degradation compound silently. **Thrash** (retraining constantly) burns
compute
and promotes noise. The triggers, the champion/challenger comparison,
and the
minimum interval are what keep CT between those poles.

The compliance angle closes the loop. Every retrain that names its
reasons,
passes its gates, and records its promotion satisfies the audit
requirement
automatically — which is why continuous training, done right, is not
just an
operational convenience but a regulatory asset. A model that rebuilds
itself
without a paper trail is a liability; one that rebuilds with full
provenance
is the strongest compliance posture available.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain why models degrade and name the three drift types
2. Distinguish schedule, drift, performance, and data triggers
3. Implement a trigger evaluator that names its reasons
4. Run the champion/challenger comparison for a retrained model
5. Explain the CT loop: detect → retrain → eval → promote
6. Avoid retrain thrash with minimum intervals and cooldowns
7. Wire CT into the registry, CI, and monitoring lifecycle

## Prerequisites

| Need | Where |
|---|---|
| Monitoring and drift (PSI) | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |
| CI gates | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |
| Pipeline orchestration | `08-mlops/lectures/09-pipeline-orchestration-lecture.md` |

## 1. Why Models Degrade

A model's accuracy is a function of a *data distribution*, and
distributions
move. Three movements matter:

- **Concept drift**: the *meaning* of the label changes (what counts as fraud
  evolves as fraudsters adapt).
- **Data drift**: the *inputs* change (a new device, a new demographic, a new
  season) while the label rule stays the same.
- **Label shift**: the *base rate* changes (more fraud overall) while the
  conditional behavior is stable.

```python
# The signature is always the same: the same model, a lower score, no code change.
degradation = {
    "launch_accuracy": 0.91,
    "month_6_accuracy": 0.84,
    "code_changed": False,
    "data_changed": True,
}
```

The lesson: a model is a snapshot of a moment. Time is a feature you did
not
train on, and it changes everything else.

## 2. The CT Loop

Continuous training is a closed loop, not a cron job:

```text
monitor → trigger → retrain → evaluate → compare → promote (or hold)
   ^                                                        |
   └────────────── the new champion is monitored ───────────┘
```

1. **Monitor** watches accuracy, drift, and data volume (Lectures 11, 19).
2. **Trigger** fires when a condition is met (section 3).
3. **Retrain** runs the pinned pipeline on fresh data (Lectures 03, 09).
4. **Evaluate** scores the challenger on the frozen set (Lecture 12).
5. **Compare** runs the champion/challenger check (section 4).
6. **Promote** registers the winner (Lecture 04) — or holds.

Every step reuses an existing gate. CT is the *composition* of the
module's
practices, not a new one.

## 3. Retraining Triggers

A trigger names *why* a retrain ran. The four standard triggers:

| Trigger | Fires when | Example |
|---|---|---|
| Schedule | a calendar interval elapses | nightly, weekly |
| Drift | PSI or a drift metric crosses a threshold | PSI > 0.25 |
| Performance | a monitored metric drops below a floor | accuracy < 0.88 |
| Data volume | enough new labeled rows arrive | 10k new rows |
| Manual | a human pulls the lever | an incident review |

```python
def should_retrain(metrics, thresholds):
    """Return the list of reasons a retrain is due (empty means hold)."""
    reasons = []
    if metrics["days_since_train"] >= thresholds["max_age_days"]:
        reasons.append("stale")
    if metrics["psi"] >= thresholds["psi"]:
        reasons.append("drift")
    if metrics["accuracy"] <= thresholds["min_accuracy"]:
        reasons.append("performance")
    if metrics["new_rows"] >= thresholds["min_new_rows"]:
        reasons.append("data")
    return reasons
```

The reasons list is the audit trail's first line: "retrain because drift
and
data." A retrain with no named reason is indistinguishable from thrash.

## 4. Champion and Challenger

A retrained model is a *challenger*, not an upgrade. It must beat the
*champion* (the current production model) on the frozen eval set before it
promotes. This is the eval gate (Lecture 12) applied to time-triggered
candidates.

```python
def champion_challenger(challenger_acc, champion_acc, tol=0.0):
    if challenger_acc >= champion_acc - tol:
        return "promote: challenger wins"
    return "hold: champion retains"
```

The champion is the stability anchor: it prevents a noisy retrain from
replacing a good model with a worse one. Without it, CT is just
scheduled
churn.

## 5. The Retraining Pipeline

The retraining pipeline is the same pinned, idempotent DAG as Lecture
09, run
on fresh data:

```text
dvc pull (fresh version) → validate → train → evaluate → register → compare
```

Idempotency matters doubly here, because a failed retrain must be safely
re-runnable without duplicating a registry entry (Lectures 01, 03). The
pipeline
references data, code, and config by version, so any retrain is
reproducible.

The output is always a *registered candidate*, never a direct production
write.
Promotion is a separate, gated decision — the same discipline as Lecture
12.

## 6. Avoiding Retrain Thrash

Thrash is retraining so often that the system promotes noise, burns
compute,
and never settles. The guards:

- **Minimum interval**: no retrain sooner than N days after the last one,
  regardless of triggers.
- **Cooldown**: after a promotion, a quiet period before the next evaluation.
- **Significance**: the challenger must beat the champion by more than the eval
  set's noise, not just by epsilon.
- **Cost awareness**: a retrain has a dollar cost (Lecture 15); frequent
  retraining must clear a value bar.

```python
def cooldown_ok(days_since_last_retrain, min_interval_days):
    return days_since_last_retrain >= min_interval_days
```

## 7. CT in the Lifecycle

- **Monitoring (Lecture 11)**: drift and performance metrics feed the triggers.
- **Registry (Lecture 04)**: every retrain registers a candidate with its
  trigger reasons; promotion requires the gates.
- **CI (Lecture 12)**: the retrain uses the same pipeline and eval gate as a
  code-triggered build.
- **Cost (Lecture 15)**: the retrain budget is part of the cost ledger.
- **Fairness (Lecture 17)**: a retrained model is re-measured for group
  fairness before it can promote.

```python
def ct_decision(metrics, thresholds, champion_acc, challenger_acc):
    reasons = should_retrain(metrics, thresholds)
    if not reasons:
        return "hold: no trigger"
    if not cooldown_ok(metrics["days_since_train"], thresholds["min_interval_days"]):
        return "hold: cooldown"
    return champion_challenger(challenger_acc, champion_acc)
```

## 8. Data Versioning for Retrains

### Every retrain pins its inputs

A retrain is reproducible only if its data, code, and config are
versioned. The
retrain manifest records the data version (DVC hash), the code commit,
and the
training config — the same provenance discipline as Lecture 03, applied
to every
automatic rebuild.

```python
retrain_manifest = {
    "trigger_reasons": ["drift", "data"],
    "data_version": "sha256:9f...",
    "code_sha": "a1b2c3",
    "config": {"lr": 3e-4, "epochs": 50},
    "candidate_id": "v3.2.0-rc1",
}
```

### Why it matters for rollback

A retrain that cannot be reproduced cannot be audited, and a candidate
whose
inputs are unknown cannot be trusted. The manifest is also the rollback
input:
if the promoted model misbehaves, the exact retrain that produced it is
re-runnable for diagnosis.

### The audit connection

Regulated models must answer "what data trained the live model." The
retrain
manifest is that answer, generated automatically, for every automatic
rebuild —
which is the point: CT must produce audit evidence without human effort,
or it
fails compliance by design.

## 9. The Cost of Retraining

### The GPU arithmetic

A retrain costs GPU-hours: training time times the card's hourly rate,
times the
cadence. A 4-hour retrain on a $2/hr GPU, weekly, is ~$400/month —
before the
eval, storage, and monitoring. That number belongs in the cost ledger
(Lecture
15).

### The value test

A retrain is worth it if the accuracy (or business metric) gain exceeds
its cost.
A weekly retrain that recovers 0.5 points is easily justified; a daily
retrain
that moves nothing is thrash with a bill. The value test is the same as
any
engineering spend: measure the return.

### Fine-tune instead of full train

A cheaper retrain is a fine-tune on the new data from the champion's
weights,
not a full train from scratch. It costs a fraction of the GPU hours and
usually
recovers most of the drift. Full retraining is reserved for large
distribution
shifts; fine-tuning is the default CT rebuild.

### Budgeting retrains

The retrain cadence is a budget line: N retrains per month at $X each.
It is set
with the team, reviewed quarterly, and tied to the value test. An
unbounded
retrain schedule is an unbounded bill — the cost awareness from Lecture
15
applies to CT directly.

## 10. Retraining Frequency by Domain

### The spectrum

Different domains move at different speeds. Fraud models retrain daily
or
faster (adversaries adapt overnight). Recommendations retrain weekly
(tastes
shift, catalogs change). Vision models retrain monthly or on new
sensors.
Language models retrain quarterly or on new corpora. The cadence follows
the
drift rate.

### What sets it

Three inputs set the frequency: how fast the distribution moves (drift
rate),
how much new labeled data arrives (volume), and what a retrain costs
(GPU hours
and eval). Fast drift plus cheap retrains means frequent; slow drift
plus
expensive retrains means rare.

### The default

Weekly schedule plus drift/performance/data triggers, tuned per domain
from
there. The schedule is the floor that guarantees freshness; the triggers
catch
what the schedule misses. Together they are the complete cadence — and
the
minimum interval keeps them from becoming thrash.

## Every Use Case

- **Every production model**: a scheduled retrain cadence (nightly/weekly) at
  minimum.
- **Every drift alert**: a retrain evaluation, not necessarily a promotion.
- **Every performance drop**: an automatic challenger build.
- **Every data milestone**: new labeled volume triggers a retrain check.
- **Every incident review**: a manual trigger with a recorded reason.
- **Every regulated model**: triggers, reasons, and promotions in the audit trail.
- **Every cost review**: the retrain cadence justified against its dollar cost.

## Real-World Use Cases for AI Engineers

- **Fraud engineer**: concept drift is constant (attackers adapt), so the drift
  trigger fires monthly; the champion/challenger gate rejects noisy challengers
  that would have replaced a good model.
- **Recommendation engineer**: a weekly schedule plus a data-volume trigger; the
  minimum interval prevents the weekend's thin data from promoting a weak model.
- **Vision engineer**: a new camera model shifts the input distribution (data
  drift); the drift trigger fires, the retrain pipeline runs on the new sensor's
  data, and the challenger promotes only after beating the champion.
- **Platform engineer**: CT is a shared scheduled workflow with per-team
  thresholds; teams tune their trigger reasons without forking the pipeline.
- **Regulated-models engineer**: every retrain's reasons, gates, and promotion
  decision are recorded, so the audit trail answers "why is this model live."

## Common Mistakes to Avoid

### Mistake 1: No retraining at all
Silent degradation compounds. A schedule, at minimum, is non-negotiable.

### Mistake 2: Retraining on a timer with no gates
A scheduled retrain that auto-promotes is scheduled churn. Triggers
start the
build; gates decide the promotion.

### Mistake 3: Promoting the challenger without comparison
A fresh model is not a better model. Champion/challenger is mandatory.

### Mistake 4: No cooldown, constant thrash
Retraining daily on noise promotes noise and burns budget. Minimum
intervals.

### Mistake 5: Retraining on unversioned data
A retrain whose data version is unknown is irreproducible. Pin it
(Lecture 03).

### Mistake 6: Skipping fairness on retrain
A retrained model can reintroduce bias. Re-measure group fairness
(Lecture 17).

### Mistake 7: No recorded reason
A retrain with no named trigger is indistinguishable from thrash in an
audit.

## Best Practices

1. Run a scheduled retrain cadence as the floor, triggers on top
2. Name every retrain's trigger reasons; record them
3. Compare every challenger to the champion before promoting
4. Enforce a minimum interval and a post-promotion cooldown
5. Pin data, code, and config versions for every retrain
6. Use the same eval gate and fairness gate as code-triggered builds
7. Price the retrain cadence and justify it against the value
8. Require the challenger to beat noise, not just the champion by epsilon
9. Monitor the new champion from the moment it promotes
10. Keep the retrain pipeline idempotent so failures are safely re-runnable

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Trigger evaluation | seconds | O(metrics) | — |
| Retrain (full) | minutes-hours | O(data + model) | fine-tune instead of full train |
| Champion/challenger eval | O(eval set) | O(1) | smoke eval, then full |
| Registry + promotion | seconds | O(model) | — |
| Thrash (avoided) | saved GPU days | — | minimum intervals |

## AI Engineering Relevance

**Where this shows up:** any model whose world moves — fraud, recommendations,
vision, language. CT is how the model stays current without a human
remembering
to rebuild it.

| Concept here | Used for |
|---|---|
| Triggers | Named reasons to rebuild |
| Champion/challenger | Safe promotion under time pressure |
| CT loop | The self-refreshing system |
| Thrash guards | Compute and stability discipline |
| Audit trail | Proving why each model is live |

**Scale note:** at one model CT is a cron job with gates; at fifty it is a
scheduled platform where per-team thresholds tune a shared pipeline. The
trigger
reasons and the champion reference are what keep fifty self-refreshing
models
auditable.

## Practice Exercises

### Exercise 1: Trigger Evaluator (Easy)
Implement `should_retrain(metrics, thresholds)` returning the list of
reasons;
test the stale, drift, performance, data, and hold cases.

### Exercise 2: Champion/Challenger (Medium)
Implement `champion_challenger(challenger_acc, champion_acc, tol)` and
the
promote/hold/tie cases.

### Exercise 3: CT Decision (Medium)
Implement `ct_decision(metrics, thresholds, champion_acc,
challenger_acc)`
combining triggers, cooldown, and comparison; test each branch.

### Exercise 4: Thrash Guard (Hard)
Implement a cooldown + significance check so a marginally-better
challenger on
noisy data does not promote; write the thrash scenario as a
failing-then-passing
test.

## Summary

| Concept | Description |
|---|---|
| Degradation | Concept, data, and label drift move accuracy down over time |
| CT loop | Monitor → trigger → retrain → evaluate → compare → promote |
| Triggers | Schedule, drift, performance, data, manual — always named |
| Champion/challenger | The challenger must beat the champion to promote |
| Thrash guards | Minimum intervals, cooldowns, significance, cost |

Continuous training is how a model stays good after launch: rebuild on
signal,
compare against the champion, promote only winners, and record every
reason.
It is the composition of monitoring, orchestration, gating, and the
registry —
the lifecycle closing on itself.

## Quick Reference

| Task | Idiom |
|---|---|
| Trigger check | `should_retrain(metrics, thresholds)` returns reasons |
| Compare | challenger must beat champion on the frozen set |
| Avoid thrash | minimum interval + cooldown + significance |
| Reproduce | pin data/code/config for every retrain |
| Audit | record triggers, gates, and the promotion decision |

## Next Steps

Next: **[21 Deployment
Strategies](21-deployment-strategies-lecture.md)** — shadow,
canary, blue-green, and A/B.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://mlflow.org/docs/latest/model-registry.html




