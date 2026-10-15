# Quiz 01: Deployment Strategies

## Topic Overview
This quiz covers deployment fundamentals for AI services: strategy selection across recreate, rolling, blue-green, and canary; Kubernetes workload objects, Services, and Ingress; the three probes and their failure modes; requests, limits, QoS, and autoscaling; rollout and rollback mechanics; GitOps versus push delivery; observability with SLOs and error budgets; production secrets; and recovery targets with RTO and RPO.

---

## Questions

### Question 1
**Which deployment strategy stands up a complete second stack, verifies it, and then switches traffic in a single change?**

- A) Rolling update
- B) Blue-green deployment
- C) Recreate strategy
- D) Canary deployment

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Blue-green deploys the new version ("green") beside the live one ("blue"), verifies it out of band, then repoints the Service selector. Rollback is the same one-line repoint. The cost is double capacity during the window, and any state the two versions share must be migration-compatible in both directions.
</details>

---

### Question 2
**With `replicas: 4`, `maxSurge: 1`, and `maxUnavailable: 0`, what does a rolling update guarantee during the entire rollout?**

- A) The cluster briefly runs 8 replicas
- B) The old pods are terminated before new pods start
- C) Available capacity never drops below the desired replica count
- D) The rollout completes in exactly one wave

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `maxUnavailable: 0` forbids dropping below the desired count, and `maxSurge: 1` allows one pod above it. The controller adds before it subtracts, so capacity never dips; the price is one extra pod of resources for the duration of the rollout.
</details>

---

### Question 3
**Which Kubernetes workload object should run a database that needs stable pod names, ordered startup, and a persistent volume per pod?**

- A) StatefulSet
- B) Deployment
- C) DaemonSet
- D) Job

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** StatefulSet gives each pod a stable DNS name, starts and stops pods in order, and binds a `volumeClaimTemplate` claim to each ordinal so storage follows the pod across restarts. A Deployment treats pods as interchangeable, which is exactly wrong for a database with peers and identity.
</details>

---

### Question 4
**What happens when a pod fails its readiness probe?**

- A) The container is restarted
- B) The pod is deleted and rescheduled
- C) The whole node is cordoned
- D) The pod is removed from Service endpoints but keeps running

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Readiness gates traffic, not life. A failing readiness probe pulls the pod out of the Service's endpoint set so no new requests reach it, while the process keeps running and retries until it becomes ready again. Restarting is the liveness probe's job.
</details>

---

### Question 5
**A service that loads a 20-second embedding model on startup deploys with liveness and readiness probes but no startup probe. What do users see?**

- A) CrashLoopBackOff until the model finishes loading
- B) Requests failing while the pod runs but is not yet ready
- C) The pod is scheduled but never starts
- D) Nothing; probes wait for the model automatically

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The pod is alive but fails readiness during warm-up, so it receives no traffic. Without a startup probe, whether that window is harmless depends on `initialDelaySeconds` and probe timing: too aggressive and liveness kills the pod into a CrashLoopBackOff, too loose and real hangs survive. A startup probe makes the boot budget explicit.
</details>

---

### Question 6
**Why is pointing a liveness probe at the database a bad idea?**

- A) Database checks are slower than HTTP checks
- B) Kubernetes forbids liveness probes from using TCP
- C) A database outage restarts every app pod, amplifying the incident
- D) Liveness probes only run once at pod creation

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Liveness failure means "restart this container." If the probe tests a shared dependency, the dependency's outage restarts all replicas simultaneously, and each cold start adds load to the dying database. Dependency checks belong in readiness (stop sending traffic) or in alerting (wake a human), never in liveness.
</details>

---

### Question 7
**An HPA is configured with `targetCPUUtilization: 70`. What is the 70% measured against?**

- A) The container's CPU limit
- B) The CPU capacity of the node
- C) The CPU allocated to the node by the cloud provider
- D) The total CPU usage of the namespace

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Resource utilization in HPA metrics is percentage of the container's CPU **request**, not its limit and not the node. That is why dishonest requests break autoscaling: requests of `10m` make a saturated pod look idle, so the HPA divides by a fantasy number and scales far too late.
</details>

---

### Question 8
**A service autoscales correctly under traffic spikes but thrashes during quiet periods, adding and removing replicas every few minutes. What is the best fix?**

- A) Lower `minReplicas` to 1
- B) Increase the HPA's target utilization above 90%
- C) Switch the HPA metric from CPU to memory
- D) Set a longer stabilization window on scale-down

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Scale-up should be fast and scale-down deliberately slow, because pod termination interrupts in-flight work and cold starts cost latency. `behavior.scaleDown.stabilizationWindowSeconds` keeps the HPA at the highest recommended replica count over the window, absorbing normal metric jitter. Raising the target or cutting minReplicas changes where it thrashes, not whether it does.
</details>

---

### Question 9
**A team runs `kubectl rollout undo` after a bad release and discovers the deployment returns nothing to roll back to. Which misconfiguration caused it?**

- A) `progressDeadlineSeconds` was exceeded
- B) `revisionHistoryLimit` was set to 0
- C) The Service selector was changed
- D) `maxUnavailable` was set to 0

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Rollback restores a previous revision, and each revision is stored as an old ReplicaSet. `revisionHistoryLimit: 0` garbage-collects those ReplicaSets as soon as the rollout completes, deleting the very objects `rollout undo` restores. Exceeded deadlines pause a rollout; they never erase history.
</details>

---

### Question 10
**A pod sets `requests` equal to `limits` for every container. What is its QoS class and its fate under node memory pressure?**

- A) Burstable; evicted after BestEffort pods
- B) BestEffort; evicted first
- C) Guaranteed; evicted last
- D) Guaranteed; evicted first because it uses its full allocation

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Matching requests and limits marks the pod Guaranteed, meaning the scheduler reserves exactly what the cgroup enforces, so the pod cannot be starved by neighbors. Kubernetes evicts BestEffort first, then Burstable, and Guaranteed pods last. The reservation costs capacity, which is why it belongs on pods whose loss matters.
</details>

---

### Question 11
**A database takes a `pg_dump` every hour and has no continuous archiving. What RPO can it honestly claim?**

- A) At most 60 minutes
- B) Zero, because a dump is a complete copy
- C) At most 60 seconds
- D) RPO is a property of backups, not of databases

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** RPO is measured from the last recoverable copy to the moment of failure. With hourly dumps, up to 59 minutes of transactions can exist only in the dying database. Claiming a smaller RPO requires finer-grained recovery data, such as continuous WAL archiving, and every claim should be proven by a restore drill.
</details>

---

### Question 12
**What is the core difference between push-based CI/CD deployment and a GitOps pull model?**

- A) Pull models cannot run database migrations
- B) In the pull model, an in-cluster operator holds cluster credentials and reconciles against Git; in the push model, the CI system holds them
- C) Push models deploy faster because they skip the cluster
- D) Pull models require a separate cluster per environment

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The credential boundary is the difference. Push delivery gives the CI runner a kubeconfig and applies manifests once; anything applied later by anyone else is invisible to it, so live state drifts from Git unnoticed. GitOps moves the credentials inside the cluster, where an operator continuously diffs live state against the repo and reverts drift, making Git history the audit log and `git revert` the rollback.
</details>

---

### Question 13
**Why is `kubectl create secret` output insufficient for storing credentials in a GitOps repository?**

- A) It produces invalid YAML
- B) It stores the value in plaintext inside the manifest
- C) It stores only base64, which anyone with `get secret` access can decode
- D) It cannot be applied to a cluster

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** A Kubernetes Secret's `data` field is base64, an encoding designed for transport, not secrecy. Anyone who can read Secrets in the namespace, or who can read the committed manifest, recovers the plaintext. Sealed Secrets (or an external secrets operator) encrypt with the cluster's public key so the ciphertext is safe to commit and only the in-cluster controller can decrypt it.
</details>

---

### Question 14
**What must exist before an automated canary can promote or abort a release without a human?**

- A) A second cluster and a blue-green switch
- B) A canary pod on every node
- C) A Service mesh and nothing else
- D) A metric with a threshold, traffic splitting, and an automated rollback path

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** A canary is an experiment, and experiments need an instrumented decision: a metric (error ratio or latency) with a threshold that defines failure, a way to route a traffic slice to the new version, and a controller that aborts when the threshold trips. Without the metric and the abort, a "canary" is just a slow manual deploy with extra steps.
</details>

---

### Question 15
**A service has an SLO of 99.9% successful requests over 30 days. The error budget is exhausted. What should happen next?**

- A) Freeze risky releases and spend capacity restoring reliability before spending more budget
- B) Raise the SLO target so the budget resets
- C) Widen the canary from 5% to 100% while the service is healthy enough
- D) Ignore it; 0.1% is within noise

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The error budget is the shared currency between shipping and reliability. An exhausted budget means the quarter's allowance for failure is spent, so the correct move is to stop consuming it on risky changes and pay it back with fixes, then resume releases as it regenerates. Raising the SLO or widening deploys burns the remaining trust faster; 43 minutes of monthly failure is a commitment, not noise.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Easy | | |
| 5 | Medium | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Hard | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Easy | | |
| 12 | Hard | | |
| 13 | Easy | | |
| 14 | Medium | | |
| 15 | Medium | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | C | 11 | A |
| 2 | C | 7 | A | 12 | B |
| 3 | A | 8 | D | 13 | C |
| 4 | D | 9 | B | 14 | D |
| 5 | B | 10 | C | 15 | A |

---

*Generated for ai-engineer-lab - Quiz 01 of 01*
