# Glossary: Deployment Strategies

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Rolling Update | Replaces pods in waves until all run the new version | Tune maxSurge and maxUnavailable together |
| Recreate Strategy | Stops all old pods, then starts new ones | Honest downtime; safe for single writers |
| Blue-Green Deployment | Stands up a full second stack, then switches traffic | Instant rollback, double capacity |
| Canary Deployment | Sends a traffic slice to the new version first | Needs a metric and an abort rule |
| Deployment | Kubernetes workload object for stateless pods | Owns the update strategy and revisions |
| ReplicaSet | Keeps a desired count of identical pods | Each rollout revision is one ReplicaSet |
| StatefulSet | Workload object with stable identity and storage | Ordered start, per-pod volume claims |
| Service | Stable virtual IP and DNS selecting ready pods | Only ready pods receive traffic |
| Ingress | Host and path routing above Services | One TLS termination point for many services |
| Liveness Probe | Test that asks if the container is wedged | Failure restarts the container |
| Readiness Probe | Test that asks if the pod can serve traffic | Failure removes it from endpoints only |
| Startup Probe | Test that gates boot for slow-starting processes | Disables the other probes until it passes |
| Resource Request | Capacity the scheduler reserves for a container | Denominator for HPA utilization math |
| Resource Limit | Hard ceiling enforced by the cgroup | Memory excess kills; CPU excess throttles |
| QoS Class | Guaranteed, Burstable, or BestEffort ranking | Decides who is evicted first |
| Horizontal Pod Autoscaler | Scales pod count from a metric target | Works only if requests are honest |
| GitOps | Desired state in Git, reconciled by an operator | Git history is the audit log |
| Service Level Objective | Error-rate or latency target over a window | Turns thresholds into commitments |
| Error Budget | The failure allowance left by an SLO | Spend it on releases, freeze when empty |
| Recovery Time Objective | How long a system may be down | Measured only by restore drills |
| Recovery Point Objective | How much data may be lost, in time | Drives backup cadence |
| Sealed Secret | Secret ciphertext committed safely to Git | Only the cluster controller can decrypt |

---

## Detailed Definitions

### Rolling Update

**Definition:** The default Kubernetes update strategy. The Deployment controller creates pods above the desired count (maxSurge), waits for them to pass readiness, then terminates old pods down to the desired count (maxUnavailable), repeating until every pod runs the new image.

**Example:**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # at most one extra pod during the wave
    maxUnavailable: 0   # never drop below the desired count
minReadySeconds: 10     # count a new pod ready only after 10s of stability
```

**Related Terms:** Deployment, maxSurge, Readiness Probe, ReplicaSet

**Key Facts:**
- `maxSurge: 0, maxUnavailable: 1` trades capacity for speed and can cause downtime at `replicas: 1`
- With `maxUnavailable: 0`, a 6-replica rollout creates pods one at a time in the worst case
- `minReadySeconds` catches pods that pass a probe and then immediately crash
- Rollback is the same mechanism running in reverse, bounded by readiness

---

### Recreate Strategy

**Definition:** A strategy that terminates every old pod before creating any new one. It guarantees no two versions run simultaneously, at the cost of a full downtime window during the swap.

**Example:**
```yaml
strategy:
  type: Recreate
```

**Related Terms:** Rolling Update, StatefulSet, Blue-Green Deployment

**Key Facts:**
- The right choice when two versions writing to one store would corrupt state
- Downtime equals old-pod termination time plus new-pod startup time
- Blue-Green solves the same problem without downtime, by paying for a second stack
- Dev and staging environments often use recreate because simplicity beats availability there

---

### Blue-Green Deployment

**Definition:** A strategy that deploys the complete new version alongside the live one, verifies it, then repoints the Service or Ingress selector to it in a single change. Rollback is repointing back.

**Example:**
```
before:  Service → selector app=auth,ver=blue   →  [blue][blue][blue]
deploy:  [green][green][green] added and smoke-tested
switch:  Service → selector app=auth,ver=green  →  [green][green][green]
undo:    Service → selector app=auth,ver=blue   (one manifest change)
```

**Related Terms:** Rolling Update, Canary Deployment, Service

**Key Facts:**
- Costs double capacity for the duration of the release window
- Schema changes must be expand-then-contract, or the rollback cannot read what green wrote
- The switch is instant only if the traffic layer caches nothing (connection pools, DNS TTL)
- Verification must happen before the switch; after it, users are the test suite

---

### Canary Deployment

**Definition:** A strategy that routes a small percentage of traffic to the new version, widens the percentage while metrics hold, and aborts on threshold breach. The deployment itself becomes an experiment.

**Example:**
```yaml
# Outline of an Argo Rollouts analysis
analysis:
  interval: 1m
  maxWeight: 50
  stepWeight: 10
  metrics:
    - name: error-rate
      threshold: 1
      query: |
        sum(rate(http_requests_total{status=~"5.."}[2m]))
        / sum(rate(http_requests_total[2m]))
```

**Related Terms:** Blue-Green Deployment, Service Level Objective, GitOps

**Key Facts:**
- Requires three pieces: a metric with a threshold, traffic splitting, and automated abort
- Without metrics it is a slow manual deploy wearing a safer name
- Start at 1% to 5% of traffic; widen only on success, never on a timer alone
- The audience for a canary is the dashboards, not the users

---

### Deployment

**Definition:** The Kubernetes workload object for stateless services. It declares replicas, an update strategy, and a pod template, and it manages ReplicaSets to reconcile toward that declaration.

**Example:**
```bash
# Create, watch, and inspect a Deployment
kubectl apply -f deployment.yaml
kubectl rollout status deployment/devmate-api -n devmate
kubectl rollout history deployment/devmate-api -n devmate
```

**Related Terms:** ReplicaSet, Rolling Update, StatefulSet

**Key Facts:**
- `spec.selector.matchLabels` must match the pod template labels or apply is rejected
- Every template edit creates a new revision, recorded as a new ReplicaSet
- Scaling replicas does not create a revision; changing the template does
- `revisionHistoryLimit` (default 10) is how far `rollout undo` can reach back

---

### ReplicaSet

**Definition:** The object that maintains a stable set of identical pods, creating replacements when pods die. Deployments manage ReplicaSets; you rarely create one directly.

**Example:**
```bash
# One revision, one ReplicaSet: see them during a rollout
kubectl get replicasets -n devmate -l app=devmate-api
# NAME                        DESIRED   CURRENT   READY
# devmate-api-7f4c9d8b6       3         3         3    # old revision
# devmate-api-5b8a6e2d1       3         3         0    # new revision
```

**Related Terms:** Deployment, Rolling Update

**Key Facts:**
- Deleting a Deployment garbage-collects its ReplicaSets and their pods
- The old ReplicaSet is scaled to zero, not deleted, until history prunes it
- Old revisions are what `rollout undo --to-revision=N` restores
- Direct ReplicaSet edits fight the Deployment controller; do not do it

---

### StatefulSet

**Definition:** A workload object for processes that need stable identity: ordered startup and shutdown, a predictable DNS name per pod, and a persistent volume claim that follows each pod across restarts.

**Example:**
```yaml
spec:
  serviceName: "qdrant"
  replicas: 3
  volumeClaimTemplates:
    - metadata: { name: data }
      spec:
        accessModes: ["ReadWriteOnce"]
        resources: { requests: { storage: 10Gi } }
```

**Related Terms:** Deployment, Service, Resource Request

**Key Facts:**
- Pod 2 starts only after pod 0 and pod 1 are ready, and stops in reverse order
- Deleting pod 0 does not delete its volume; the replacement reattaches the same claim
- Peers find each other through `<pod>.<serviceName>.<namespace>.svc`
- Rolling updates are one pod at a time, by design

---

### Service

**Definition:** A stable virtual IP address and DNS name that selects pods by label and load-balances across the ones currently passing readiness. Pod IPs are ephemeral; the Service is not.

**Example:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: devmate-api
  namespace: devmate
spec:
  type: ClusterIP
  selector: { app: devmate-api }
  ports:
    - port: 80
      targetPort: 8000
```

**Related Terms:** Ingress, Readiness Probe, Deployment

**Key Facts:**
- ClusterIP is internal; LoadBalancer asks the cloud for a public endpoint
- Endpoints are recomputed from readiness results, not from pod existence
- Services provide DNS: `devmate-api.devmate.svc.cluster.local` resolves to the virtual IP
- Headless Services (`clusterIP: None`) return pod IPs directly, which StatefulSets use

---

### Ingress

**Definition:** An HTTP routing layer above Services, matching requests by hostname and path and terminating TLS in one place instead of per service.

**Example:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fslab
spec:
  rules:
    - host: api.example.org
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: auth-service
                port: { number: 80 }
```

**Related Terms:** Service, Liveness Probe

**Key Facts:**
- An Ingress is a rule set; an ingress controller implements it (NGINX, Traefik, cloud LB)
- One certificate can cover every host routed through the controller
- Backend pods are eligible only while they pass readiness
- Ingress routes HTTP(S); TCP and UDP need a LoadBalancer Service or a Gateway

---

### Liveness Probe

**Definition:** A periodic test asking whether the process is wedged beyond recovery. A failing liveness probe restarts the container.

**Example:**
```yaml
livenessProbe:
  httpGet: { path: /health, port: 8000 }
  periodSeconds: 15
  failureThreshold: 3   # 45 seconds of failure before a restart
```

**Related Terms:** Readiness Probe, Startup Probe, QoS Class

**Key Facts:**
- Never point it at a downstream dependency; that restarts your app for someone else's outage
- A liveness check under load becomes a restart storm, which looks like an outage amplifier
- Use startup probes instead of long `initialDelaySeconds` for slow boots
- Failure means restart, so every false positive costs a cold start

---

### Readiness Probe

**Definition:** A periodic test asking whether the pod can accept traffic right now. A failing readiness probe removes the pod from Service endpoints while the container keeps running.

**Example:**
```yaml
readinessProbe:
  httpGet: { path: /ready, port: 8000 }
  periodSeconds: 10
  failureThreshold: 3   # 30 seconds out of rotation, no restart
```

**Related Terms:** Liveness Probe, Service, Startup Probe

**Key Facts:**
- It is the mechanism that makes rolling updates safe: new pods join only when ready
- A pod failing readiness during a deploy simply waits; it does not crash
- Model warm-up, index loading, and pending migrations belong here, not in liveness
- `/ready` may check dependencies (database reachable); `/health` should not

---

### Startup Probe

**Definition:** A probe that runs until it succeeds, disabling liveness and readiness for that container while it boots. It exists for processes whose startup time exceeds normal probe patience.

**Example:**
```yaml
startupProbe:
  httpGet: { path: /health, port: 8000 }
  periodSeconds: 10
  failureThreshold: 30   # tolerate up to 300 seconds of boot time
```

**Related Terms:** Liveness Probe, Readiness Probe

**Key Facts:**
- It replaces the `initialDelaySeconds` guessing game with an explicit budget
- Once it passes, liveness and readiness take over at their own intervals
- If it never passes, the container is killed; that is a boot failure, reported as such
- AI services that load model weights on start almost always need one

---

### Resource Request

**Definition:** The amount of CPU and memory the scheduler reserves for a container when placing it on a node. It is also the denominator in HPA utilization calculations.

**Example:**
```yaml
resources:
  requests:
    cpu: 250m
    memory: 512Mi
```

**Related Terms:** Resource Limit, QoS Class, Horizontal Pod Autoscaler

**Key Facts:**
- Too low and nodes oversubscribe; pods get evicted under memory pressure
- Too high and you pay for capacity nothing uses; the autoscaler adds nodes for ghosts
- Measure from real usage (p95 of steady state), then add headroom deliberately
- Requests, not limits, decide scheduling and HPA behavior

---

### Resource Limit

**Definition:** The hard ceiling a container cannot exceed, enforced by cgroups. Exceeding the memory limit kills the process; exceeding the CPU limit throttles it.

**Example:**
```yaml
resources:
  limits:
    cpu: "1"
    memory: 1Gi
```

**Related Terms:** Resource Request, QoS Class

**Key Facts:**
- Memory overage is an OOM kill; CPU overage only slows the process down
- An OOM kill looks like a crash, so pair limits with a memory metric on the dashboard
- CPU throttling looks like a latency incident; the cause is invisible without `container_cpu_cfs_throttled`
- Limits without requests still create a Burstable pod, not a protected one

---

### QoS Class

**Definition:** A priority ranking Kubernetes assigns from a pod's requests and limits. It decides which pods are evicted first when a node runs out of memory.

**Example:**
```yaml
# Guaranteed: every container sets requests == limits
resources:
  requests: { cpu: "1", memory: 1Gi }
  limits:   { cpu: "1", memory: 1Gi }
# -> status.qosClass: Guaranteed
```

**Related Terms:** Resource Request, Resource Limit

**Key Facts:**
- Guaranteed pods are evicted last, Burstable next, BestEffort first
- BestEffort means no requests and no limits at all; those pods die immediately under pressure
- Databases and quorum members deserve Guaranteed; bursty workers can be Burstable
- QoS costs nothing to set and decides survival during a node incident

---

### Horizontal Pod Autoscaler

**Definition:** A controller that changes the replica count of a workload so a metric stays near a target, most often CPU utilization measured against requests.

**Example:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: devmate-api-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: devmate-api }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
```

**Related Terms:** Resource Request, Deployment, VPA

**Key Facts:**
- `averageUtilization: 70` means 70% of requests; dishonest requests break the math
- Give scale-up a short stabilization window and scale-down a long one, or replicas flap
- The cluster autoscaler only adds nodes if pending pods can be spread across zones
- Pair with `topologySpreadConstraints` so replicas are not all on one node

---

### GitOps

**Definition:** A delivery model where the desired state of the cluster lives in Git and an in-cluster operator continuously reconciles live state against it.

**Example:**
```
push model:  CI runner (holds kubeconfig) --kubectl apply--> cluster
GitOps:      cluster operator --watch repo--> diff live vs Git --apply--> cluster
```

**Related Terms:** Deployment, Sealed Secret, Rolling Update

**Key Facts:**
- Drift is detected and reverted instead of accumulating unnoticed
- A pull request is the change review; Git history is the audit log; revert is the rollback
- Cluster credentials stay inside the cluster instead of living in CI
- Every change must be committable, which is why secrets need sealing or external storage

---

### Service Level Objective

**Definition:** A measurable reliability target for a service over a defined window, such as 99.9% of requests succeeding in a rolling 30 days, evaluated against an indicator sampled continuously.

**Example:**
```yaml
# SLO: 99.9% successful requests over 30 days
- alert: FastErrorBudgetBurn
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      / sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)
  for: 2m
  labels: { severity: page }
```

**Related Terms:** Error Budget, Canary Deployment

**Key Facts:**
- An SLO names the indicator, the target, and the window; missing any one of the three is a goal, not an SLO
- Thresholds like "p95 over 2s" are symptoms; the SLO is the commitment behind them
- Burn-rate alerts fire on how fast the budget is consumed, not on a fixed number
- Set the SLO slightly below what you currently achieve, or it measures nothing

---

### Error Budget

**Definition:** The failure allowance implied by an SLO: the percentage of requests or time you may lose while still meeting the target, over the SLO's window.

**Example:**
```
SLO 99.9% over 30 days
  30 days = 43,200 minutes
  budget  = 0.1% x 43,200 = 43.2 minutes of allowed failure

budget full   -> ship risky releases
budget spent  -> freeze deploys, fix reliability first
```

**Related Terms:** Service Level Objective, Canary Deployment

**Key Facts:**
- The budget is shared vocabulary between engineering and product: it prices risk in minutes
- Fast burn (14.4x the steady rate for 1h) pages; slow burn (1x for 6h) tickets
- A canary that consumes budget faster than it buys learning should be aborted
- Without a budget, "should we ship?" degrades into opinion

---

### Recovery Time Objective

**Definition:** The maximum acceptable duration a system may be down after a failure, written down before the failure so it can be tested.

**Example:**
```
component      RTO        how it is met
API pods       < 1 min    3 replicas, readiness-gated rolling update
Node loss      < 5 min    replicas spread across nodes
Full region    < 1 hr     second region, DNS failover, warm standby
```

**Related Terms:** Recovery Point Objective, Deployment

**Key Facts:**
- An RTO you have never measured is a wish; restore drills produce the number
- Replicas, spread, and autoscaling attack downtime; backups attack data loss
- RTO includes the detection and decision time, not just the restore time
- Different components deserve different targets; one blanket number misleads

---

### Recovery Point Objective

**Definition:** The maximum acceptable amount of data loss after a failure, expressed as elapsed time since the last recoverable copy.

**Example:**
```
last backup            failure              restored
     |                     |                    |
     +---- data lost ------+                    |  <- RPO
                         +------ downtime ------+  <- RTO

hourly pg_dump  -> RPO <= 60 min
WAL archiving   -> RPO <= minutes
```

**Related Terms:** Recovery Time Objective, GitOps

**Key Facts:**
- Backup cadence is derived from RPO; an hourly cron cannot deliver a 5-minute RPO
- A backup you have never restored is a hypothesis, not a recovery plan
- Immutable infrastructure lowers RTO; it says nothing about RPO
- State on named volumes survives a container restart, but only until someone deletes the volume

---

### Sealed Secret

**Definition:** A Kubernetes Secret encrypted with a cluster-specific public key, safe to commit to Git, decrypted only by the sealed-secrets controller running inside the cluster.

**Example:**
```bash
# Seal a plaintext secret locally; only ciphertext reaches Git
kubeseal --format=yaml < db-secret.yaml > db-sealed.yaml
kubectl apply -f db-sealed.yaml
# Rotation: reseal and commit; the controller rewrites the live Secret
```

**Related Terms:** GitOps, Resource Limit

**Key Facts:**
- Plain Secrets are base64, which anyone with `get secrets` can decode; they are dev-grade only
- Each cluster has its own certificate, so ciphertext from one cluster is useless in another
- Git history holds no plaintext, which is what makes GitOps with secrets survivable
- Alternatives for different constraints: External Secrets Operator, Vault, a platform vault like the one implied by `sync: false` entries in `render.yaml`

---

## Summary

These terms cover the vocabulary you need to release and operate production AI services:

1. **Strategies are risk decisions.** Rolling, recreate, blue-green, and canary trade downtime, capacity, and rollback speed differently; choose on purpose.
2. **The workload object encodes failure behavior.** Deployment for interchangeable pods, StatefulSet for identity, Job for run-to-completion work.
3. **Probes are three different questions.** Startup gates boot, readiness gates traffic, liveness gates restarting; confusing them causes restart storms.
4. **Requests are a promise, limits are a blast radius.** Together they set your QoS class, your scheduler placement, and your HPA arithmetic.
5. **Reversibility is a feature you can delete.** Mutable tags, empty revision history, and slow readiness each quietly disable rollback.
6. **SLOs turn opinions into budgets.** Error budgets make "should we ship?" arithmetic, and burn-rate alerts make it timely.
7. **RTO and RPO are contracts with the restore drill.** Until a backup has been restored on a clock, both numbers are guesses.

**Next:** Lecture 02 covers CI/CD with GitHub Actions (`projects/06-devops/ci-cd/`), where built images get tested, scanned, and promoted through the tiers defined here.
