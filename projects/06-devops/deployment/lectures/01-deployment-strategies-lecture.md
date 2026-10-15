# Lecture 01: Deployment Strategies for AI Services

## Topic Overview

Deployment is the discipline of moving tested code into an environment where real users depend on it, without losing availability, data, or the ability to go back. For AI services the stakes carry extra weight: an embedding model change silently invalidates a vector index, a retrieval service cold-starts slowly enough to fail health checks, and a GPU node pool costs real money while it idles. This lecture builds the full path from strategy selection (recreate, rolling, blue-green, canary) through Kubernetes objects, probes, autoscaling, rollout and rollback mechanics, progressive delivery, GitOps, observability with SLOs, production secrets, disaster recovery with explicit RTO and RPO, and the cost controls that keep a cluster affordable.

**Duration:** 4-5 hours
**Difficulty:** Intermediate
**Prerequisites:** Docker containerization fundamentals (`projects/06-devops/docker/lectures/01-containerization-lecture.md`), Linux command line, HTTP fundamentals, basic YAML

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Compare** recreate, rolling, blue-green, and canary deployments along downtime, cost, and rollback speed
2. **Model** environment tiers and the promotion path that carries one immutable artifact from commit to production
3. **Select** the Kubernetes workload object that matches a service's state and lifecycle
4. **Configure** liveness, readiness, and startup probes and predict what each failure mode does to traffic
5. **Size** resource requests and limits, name the QoS class they produce, and explain why HPA math needs requests
6. **Drive** a rollout and its rollback with `kubectl rollout`, and describe what progressive delivery adds on top
7. **Contrast** GitOps reconciliation with push-based CI/CD and defend a pull-based deploy for a cluster
8. **Instrument** a service with the RED and USE methods, then turn an SLO into alerting with an error budget
9. **Protect** production secrets with sealed secrets, an external secrets operator, or a platform vault
10. **State** a recovery target as RTO and RPO, and name the cost levers that keep a cluster affordable

---

## Key Concepts

### 1. Deployment Strategies

Every strategy is a different answer to one question: what happens to live traffic while new code arrives?

| Strategy | Downtime | Extra capacity needed | Rollback speed | Best for |
|---|---|---|---|---|
| **Recreate** | Yes, full stop | None | Slow: rebuild the old version | Databases, dev environments, stateful migrations |
| **Rolling** | None, if tuned | `maxSurge` pods | Medium: roll back through the same wave | Default for stateless services |
| **Blue-green** | None | Full second copy | Instant: flip the pointer back | High-risk releases with a clean traffic switch |
| **Canary** | None | A few canary pods | Instant: drop the canary | Changes you want metrics to judge |

**Recreate** tears every old pod down, then starts new ones. It is honest about its downtime, which is exactly why stateful systems prefer it: you never run two versions of a writer against one database.

**Rolling update** replaces pods in waves, governed by two numbers:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # pods created ABOVE the desired count during the wave
    maxUnavailable: 0  # pods allowed BELOW the desired count during the wave
```

With `replicas: 4`, `maxSurge: 1`, `maxUnavailable: 0`, a rollout runs like this:

```
Start:   [old][old][old][old]          4 old, capacity 4
Step 1:  [old][old][old][old][new]     surge to 5, wait until new is READY
Step 2:  [old][old][old][new]          kill one old, capacity 4
Step 3:  [old][old][new][new]          ...
End:     [new][new][new][new]          4 new, capacity 4
```

The order of operations matters: with `maxUnavailable: 0` the cluster always adds before it subtracts, so capacity never dips below the desired count. The cost is one extra pod of memory and CPU for the duration of the rollout. Trade surge for unavailability deliberately, never by default.

**Blue-green** stands up the complete new stack ("green") beside the live one ("blue"), verifies it, then switches the Service or Ingress selector in one move. Rollback is the same one-line switch. The hidden bill is double capacity for every release window, and the hidden trap is state: if green writes to the same database blue uses, switching back does not unwrite anything. Schema changes must be expand-then-contract: add new columns and tables first, deploy code that can read both shapes, migrate the data, then remove the old shape in a later release.

**Canary** routes a small slice of traffic to the new version, widens it on success, and aborts it on failure:

```
             ┌─── 1% traffic ──→ [v2 canary]   watch error rate + latency
[clients] ───┤                ──→ [v1 stable]
             └─── widen to 10% → 50% → 100% only while metrics hold
```

Canary is the only strategy where the deployment itself is an experiment, and it demands three things a naive setup lacks: a metric that actually detects the regression, a controller that widens or aborts without a human, and rollback that is fast enough to matter at 1% of traffic.

### 2. Environment Tiers and Promotion Paths

Environments exist to move risk out of production before production sees it.

| Tier | Infrastructure | Purpose | Auto-deploy |
|---|---|---|---|
| Local | Docker Compose | Development | No |
| Staging | Single-node cluster | Pre-production testing | Yes (on main) |
| Production | Multi-node cluster | Live traffic | Manual gate |

That table mirrors the tier model in `projects/06-devops/deployment/README.md`, which also spells out the promotion path:

```
Code Push → CI Tests → Docker Build → Push to Registry → Deploy to Staging
    → Smoke Tests → Manual Approval → Deploy to Production → Canary → Full Rollout
```

Two rules make this path trustworthy:

1. **Promote the artifact, never rebuild it.** The image digest tested in staging is the digest that runs in production. A second build produces different bytes, usually because a dependency floated to a newer version, and the test result no longer describes what you ship.
2. **Promotion is a decision, not a side effect.** Staging can deploy automatically on main. Production waits for a human or a gate: smoke tests green, migration reviewed, rollback rehearsed.

This repository's own deployment surface is deliberately small, and worth naming precisely: the real deployable artifacts are `projects/04-ai-engineering/devmate/docker/Dockerfile`, `infra/docker/docker-compose.yml`, `render.yaml`, and `projects/04-ai-engineering/devmate/railway.toml`. The `infra/k8s/` tree printed in `projects/06-devops/deployment/README.md` is a teaching example of a layout, not a directory in this repo. Learn its shape, then apply it where a cluster actually exists.

### 3. Kubernetes Workload Objects

The object you choose encodes how the workload behaves under failure. Pick by state and lifecycle, not by habit.

| Object | Use it for | Identity | Rolling update |
|---|---|---|---|
| **Deployment** | Stateless services | Interchangeable pods | Yes |
| **StatefulSet** | Databases, brokers, anything with a stable identity | Stable name, stable storage, ordered start/stop | Careful, one at a time |
| **DaemonSet** | One pod per node: log shippers, GPU device plugins, exporters | Node-bound | Node-by-node |
| **Job** | Run to completion: batch, migrations, backfills | Retries until success | Not applicable |
| **CronJob** | Scheduled Jobs: nightly reports, index rebuilds | Time-triggered | Not applicable |

A Deployment is a thin wrapper over ReplicaSets: it keeps the desired replica count and owns the update strategy, while the ReplicaSet keeps the pods alive. That indirection is why `kubectl rollout history deployment/x` works: each revision is a stored ReplicaSet.

StatefulSets refuse to be Deployment-shaped on purpose. Deleting pod 3 of 5 does not touch pod 0, volumes are claimed per pod by name, and pods get a stable DNS name so a replica can find its peers. That is what a database needs and what a stateless API finds suffocating.

One Deployment example, in the same shape the README teaches (namespace, selector, and template labels must agree):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: fslab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
        - name: auth-service
          image: ghcr.io/org/auth-service:v1.4.2@sha256:9f2c1a...
```

### 4. Services, Ingress, and Traffic Flow

Pods are disposable, so their IPs are meaningless. A Service is a stable virtual IP plus DNS name that selects pods by label and load-balances across the ones that are ready.

| Service type | What it exposes | Typical use |
|---|---|---|
| **ClusterIP** | Internal virtual IP only | Default; service-to-service calls |
| **NodePort** | A port on every node (30000-32767) | Quick external tests |
| **LoadBalancer** | A cloud load balancer | One public service at a time |
| **ExternalName** | A CNAME to an external hostname | Managed databases, SaaS APIs |

Ingress sits above Services and routes by hostname and path through one entry point, with TLS termination in one place:

```
client → cloud LB → Ingress controller → Service(devmate-api) → ready pods
                           │
                           └─→ Service(devmate-ui)            → ready pods
```

The critical link: **Ingress and Service endpoints only include pods that pass their readiness probe.** That is the mechanism behind objective 4. A pod that is running but not ready receives no traffic; a pod that is ready and then fails readiness is pulled from rotation without being killed.

### 5. Configuration, Secrets, and Storage

Separate three things that beginners dump into the container image: configuration, secrets, and state.

- **ConfigMap** holds non-sensitive configuration as key-value data, mounted as a file or injected as environment variables.
- **Secret** holds credentials. Base64 is an encoding, not encryption: anyone who can `kubectl get secret -o yaml` in the namespace can decode it. Treat a plain Secret as "conveniently shaped," not "safe." Section 13 covers the options that actually encrypt.
- **PersistentVolumeClaim** requests storage; a **StorageClass** decides what kind is provisioned (SSD, network, retention policy). The claim outlives pods, which is the entire point: a StatefulSet reattaches the same claim when it recreates a pod.

The compose file in this repo shows the environment-side equivalent of the same split: `infra/docker/docker-compose.yml:124` passes `${LANGFUSE_PUBLIC_KEY:-}` style variables through from the host environment, so keys live in a gitignored `.env` file instead of the committed file, while `infra/docker/docker-compose.yml:11` shows the anti-pattern in the same document: `POSTGRES_PASSWORD: devmate` committed in plaintext, which is acceptable for a local development stack and would be a finding in production.

### 6. Probes: Liveness, Readiness, Startup

Three probes, three different questions. Confusing them is the single most common cause of production restart loops.

| Probe | Question it answers | What a failure does | Never use it to |
|---|---|---|---|
| **livenessProbe** | Is the process wedged and unrecoverable? | Restart the container | Detect overload; that becomes a restart storm |
| **readinessProbe** | Can this pod serve traffic right now? | Remove it from Service endpoints; the pod keeps running | Gate pod startup on its own |
| **startupProbe** | Has the process finished booting? | Hold off liveness and readiness until it passes | Replace a health endpoint |

```yaml
livenessProbe:
  httpGet: { path: /health, port: 8000 }
  periodSeconds: 15
  failureThreshold: 3        # 3 failures x 15s = 45s before a restart
readinessProbe:
  httpGet: { path: /ready, port: 8000 }
  periodSeconds: 10
  failureThreshold: 3        # 30s out of rotation, no restart
startupProbe:
  httpGet: { path: /health, port: 8000 }
  periodSeconds: 10
  failureThreshold: 30       # up to 300s to boot before anything else counts
```

The failure modes, stated as behavior:

- **Missing readiness** on a service that loads an embedding model for 20 seconds means 20 seconds of 500s behind a load balancer. The pod is alive; it is not ready.
- **Missing liveness** on a service that can deadlock means it stays broken forever, still passing traffic.
- **Liveness with a long `initialDelaySeconds` instead of a startupProbe** trades one bug for another: delay too short and slow boots get killed into a CrashLoopBackOff; delay too long and genuine hangs survive.
- **Liveness that checks a downstream dependency** (database reachable) restarts the app for someone else's outage, and with several replicas becomes a thundering herd against the dying database.

The `/health` contract already exists in this repo's artifacts, which is the point of a health endpoint: `projects/04-ai-engineering/devmate/docker/Dockerfile:55` declares a Docker `HEALTHCHECK` against it with `curl -f`, `render.yaml:29` polls it as `healthCheckPath`, and `projects/04-ai-engineering/devmate/railway.toml:12` does the same on Railway. Kubernetes probes are the third consumer of the same endpoint.

### 7. Requests, Limits, and QoS Classes

Requests and limits answer different questions.

| Field | Question | Enforced by | When it bites |
|---|---|---|---|
| **requests** | How much does the scheduler reserve? | Scheduler (placement) | Too low: node oversubscribed, evictions. Too high: you pay for idle capacity |
| **limits** | What is the hard ceiling? | cgroup | Memory limit exceeded: OOM kill; CPU limit exceeded: throttling, not death |

Requests are a capacity-planning commitment; limits are a blast-radius control. A memory limit kills the process (OOM), a CPU limit only slows it down, which is why a CPU-starved service looks like a latency incident rather than a crash.

Set both and Kubernetes assigns a QoS class, which decides who dies first when a node runs out of memory:

| QoS | Condition | Eviction priority |
|---|---|---|
| **Guaranteed** | requests == limits for every container | Last to be evicted |
| **Burstable** | requests set, but limits differ or are missing | Middle |
| **BestEffort** | no requests or limits at all | First to be evicted |

The local stack already sets a ceiling where it matters: `infra/docker/docker-compose.yml:155` gives `devmate-api` a 2G memory limit with a 1G reservation, so a runaway ingestion cannot take the host down. That is the Compose shape of the same idea; in Kubernetes the shape is `resources.requests` and `resources.limits` on every container, which is also what the exercise's K8S002 and K8S003 rules check.

### 8. Autoscaling: HPA, VPA, and Cluster Autoscaling

Autoscaling happens at three layers, and each one fixes a different shortage:

```
        ┌── Cluster Autoscaler ── "the node pool is full"
        │     adds/removes NODES
Cluster ┤
        │     ┌── HPA ── "requests per pod are over target"
        │     │     adds/removes PODS (horizontal)
Pods ───┤─────┘
        │     ┌── VPA ── "each pod is under/over-sized
        │     │     rewrites requests (vertical)
        └─────┘     cannot share a metric with HPA)
```

The HorizontalPodAutoscaler from `projects/06-devops/deployment/README.md` (teaching example):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: auth-service }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
```

Three details decide whether this behaves:

1. **`averageUtilization: 70` is 70% of *requests*, not of the limit and not of the node.** If requests are set to 10m to squeeze more pods onto a node, the HPA divides by a fantasy number and scales far too late. Requests must be honest for autoscaling to work.
2. **Scale-up and scale-down are asymmetric on purpose.** Add a stabilization window of a minute or two upward, five minutes or more downward (`behavior.scaleDown.stabilizationWindowSeconds`), or a traffic spike becomes a replica flap.
3. **The cluster autoscaler only helps if pods can be spread.** `topologySpreadConstraints` or anti-affinity keep replicas across nodes, so adding one node actually admits the pending pod.

VPA adjusts requests instead of replica count, which is the right tool for a service with a steady footprint that was sized once and never revisited. It cannot share a metric with the HPA: both rewriting CPU targets fight each other. Run VPA in recommendation-only mode first, read the suggested values, then commit them.

### 9. Rollout and Rollback Mechanics

A rollout is a change to the pod template; Kubernetes records each change as a revision and reconciles toward it.

```bash
# Deploy a new image explicitly (records a new revision)
kubectl set image deployment/auth-service auth-service=ghcr.io/org/auth:v1.5.0 -n fslab

# Watch convergence: it blocks until status is complete or the deadline passes
kubectl rollout status deployment/auth-service -n fslab

# Inspect and undo
kubectl rollout history deployment/auth-service -n fslab
kubectl rollout undo deployment/auth-service --to-revision=3 -n fslab

# Freeze a bad rollout while you investigate, then resume
kubectl rollout pause deployment/auth-service -n fslab
kubectl rollout resume deployment/auth-service -n fslab
```

Mechanics that decide whether rollback actually works:

- **Revision history is ReplicaSets.** `revisionHistoryLimit` (default 10) controls how far back `--to-revision` can reach. Set it to 0 and you have disabled your own undo.
- **A rollout that cannot converge stops at `progressDeadlineSeconds`** (default 600s) and reports `ProgressDeadlineExceeded`. Without it, a crash-looping new version just keeps creating pods forever.
- **Rollback speed is bounded by readiness.** Undoing a bad release still has to pass the readiness probe on every pod, so a 90-second model warm-up makes every rollback 90 seconds minimum.
- **Immutable tags make rollback meaningful.** With `:latest`, "roll back" repulls the same floating tag and may deploy the same broken code, which is rule K8S001 in the exercise.

Managed platforms wrap the same idea in their own verb: this repo's runbook at `projects/04-ai-engineering/devmate/deploy/README.md:64` documents Render's one-click rollback (service → Events → Rollback to the prior deploy). The mechanics differ, the requirement does not: the previous artifact must still exist.

### 10. Progressive Delivery

Progressive delivery is canary and blue-green made declarative: you describe the analysis, and a controller runs the release like an experiment.

| Tool | What it does | Style |
|---|---|---|
| **Argo Rollouts** | Canary/blue-green traffic splitting with metric analysis and automated promotion or abort | Pull (GitOps) |
| **Flagger** | Same ideas as a Kubernetes operator, driven by Prometheus/NGINX/Istio/Linkerd traffic | Pull (GitOps) |
| **Flux** | GitOps reconciliation of the manifests themselves, including Rollouts' CRDs | Pull (GitOps) |

A canary analysis in outline:

```yaml
analysis:
  interval: 1m
  maxWeight: 50
  stepWeight: 10
  metrics:
    - name: error-rate
      threshold: 1          # abort when 5xx ratio exceeds 1%
      query: |
        sum(rate(http_requests_total{status=~"5.."}[2m]))
        / sum(rate(http_requests_total[2m]))
```

Every automated canary needs the same three pieces: a metric with a threshold (the analysis above), traffic splitting (an Ingress, service mesh, or a controller that scales the canary deployment up and down), and a rollback path that triggers on threshold breach without a human. Without metrics there is no canary, only a slow manual deploy.

### 11. GitOps versus Push CI/CD

Both pipelines move the same artifact; they differ in who holds the credentials to the cluster.

```
Push model                              Pull model (GitOps)
CI runner                               Git operator inside the cluster
  │ has cluster credentials               │ has read access to Git
  ├─ build, test                          ├─ watches the repo
  ├─ kubectl apply ──→ cluster            ├─ diffs desired vs live
  └─ drift appears, nobody notices        └─ kubectl apply ──→ cluster
                                          drift is detected and reverted
```

- **Push** is simple and matches how most CI tutorials work. Its costs: the CI system holds a kubeconfig (a credential that must live somewhere long-lived), and state applied by hand or by another pipeline is invisible to it. What is on the cluster can silently diverge from what is in Git.
- **Pull (GitOps)** keeps cluster credentials inside the cluster, in an operator that reconciles the repo against live state continuously. The Git history is the audit log, a diff in a pull request is the change review, and `git revert` is the rollback. The costs: you must commit every change, including secret material via sealed/encrypted secrets, and you need tooling (Flux, Argo CD) running somewhere.

A useful rule of thumb: push CI to build and test artifacts, pull to deploy them. Neither should deploy by mutating a live cluster invisibly; if it happened, it should be because it is in Git.

### 12. Observability: Metrics, Logs, and SLOs

The stack from `projects/06-devops/deployment/README.md` is the standard shape:

| Component | Purpose | Port |
|---|---|---|
| Prometheus | Metrics collection and alert evaluation | 9090 |
| Grafana | Dashboards | 3000 |
| Alertmanager | Routing and deduplication of alerts | 9093 |
| Loki | Log aggregation, queried like metrics | 3100 |

Two method families decide what to measure:

- **RED** (Rate, Errors, Duration) applied to *services*: requests per second, error ratio, latency distribution. RED describes what users feel.
- **USE** (Utilization, Saturation, Errors) applied to *resources*: CPU and memory used, queue depth or throttling, hardware errors. USE describes where the ceiling is.

An alert rule in the README's style:

```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
  for: 5m
  labels: { severity: critical }
```

The missing half is **why 1%?** An SLO answers that: a commitment, measured over a window, such as "99.9% of requests succeed in a rolling 30 days." The remainder is the **error budget**: 0.1% of 30 days is about 43 minutes of allowed failure. That budget is the shared language between engineering and product: spend it on risky releases while it is full, freeze deploys when it is exhausted.

SLO-derived alerting beats guessed thresholds. Instead of "p95 > 2s" in isolation, alert on **burn rate**: how fast the error budget is being consumed right now (a 14-day budget burned in 1 hour means something is very wrong). The README's threshold table is a reasonable starting point, but every number in it should eventually trace back to an SLO, not to a round number someone liked.

Metrics must also be **exemplar-linked to logs**: when an error rate alert fires, you need to jump from the spike to the logs of the offending requests (Prometheus + Loki + a trace ID label is the usual chain). Metrics tell you something broke; logs tell you what.

### 13. Secrets in Production

A Kubernetes Secret is base64. Base64 is a translation, not a lock. Three approaches actually protect credentials:

| Approach | Where ciphertext lives | Who can decrypt | Operational cost |
|---|---|---|---|
| **Sealed Secrets** | Encrypted in Git, committed safely | Only the cluster's controller | Low: one controller, `kubeseal` CLI |
| **External Secrets Operator** | In a cloud secret manager (KMS, Vault, SSM) | The platform's IAM | Medium: needs a manager and IRSA/IAM wiring |
| **Vault / cloud KMS** | Encrypted at rest with rotation and audit | Authenticated, audited agents | High: worth it when compliance or rotation demands it |

Two patterns already present in this repo, one good and one deliberately local:

- `render.yaml:64` marks `GROQ_API_KEY` and friends `sync: false`, so the values are entered in the dashboard and never committed, and `render.yaml:69` generates `SECRET_KEY` rather than asking a human to paste one. This is the platform-managed equivalent of an external secrets store.
- `infra/docker/docker-compose.yml:127` interpolates `${ANTHROPIC_API_KEY:-}` from the host environment, keeping the key out of the committed file for local development.

The rule that survives every tool choice: **the value must not be readable by everyone who can read the repository**, and rotation must be a normal operation, not an incident. Committed plaintext (the `POSTGRES_PASSWORD: devmate` in the local compose file) is acceptable only where the blast radius is a local dev database.

### 14. Backup and Disaster Recovery

RTO and RPO are the two numbers that make "we have backups" a falsifiable claim:

- **RTO (Recovery Time Objective):** how long the system may be down.
- **RPO (Recovery Point Objective):** how much data may be lost, measured in time.

```
     last good backup          failure           restored
            │                    │                   │
            └──── data lost ─────┤                   │  ← RPO
                                 └──── downtime ─────┘  ← RTO
```

The README's targets, which are a good template for any service:

| Scenario | RTO | RPO |
|---|---|---|
| Pod crash | < 1 min | 0 |
| Node failure | < 5 min | 0 |
| Database corruption | < 30 min | < 1 hr |
| Full region outage | < 1 hr | < 5 min |

Backup cadence follows from RPO: an hourly `pg_dump` cannot deliver an RPO under an hour, so a database promising `< 5 min` needs continuous WAL archiving, not a cron job. Note the pairing in the README's backup matrix: `pg_dump` for logical snapshots plus WAL for the log stream, RDB snapshots for Redis, the Qdrant Snapshot API, and etcd for cluster state.

Two failure modes to design against:

1. **The untested backup.** A backup you have never restored is a hypothesis. Schedule restore drills: provision a clean environment, restore, verify row counts and a sample query, measure the clock. The drill is what turns RTO from aspiration into a measured number.
2. **State that dies with the container.** In this repo, databases write to named volumes declared at `infra/docker/docker-compose.yml:213`, which survive `docker compose down` but are destroyed by `down -v`. Anything you would hate to lose belongs on a volume with a backup policy, not in a container filesystem.

### 15. Cost Control

Managed Kubernetes bills for the nodes you reserve, not the CPU you use, so the first lever is sizing requests honestly:

| Lever | Typical saving | Risk |
|---|---|---|
| Right-size `requests` against real usage | 20-40% of node cost | Undersizing causes evictions and HPA misfires |
| Cluster autoscaler with scale-down delay | Removes idle nodes automatically | Cold starts when scaling back up |
| Spot/preemptible nodes for fault-tolerant pools | 60-80% on that pool | 30-60s interruption notice; needs graceful shutdown |
| Persistent volume right-sizing and storage classes | Storage line item | Too-small volumes block writes |
| Retention limits on logs, metrics, traces | Observability stack cost | Losing forensic history you later need |
| Small, frequent releases | Smaller images, faster rollouts | None, if CI is disciplined |

This repo is a small example of the same thinking: `render.yaml:50` sets tight rate limits (`RATE_LIMIT_REQUESTS: 20`) to protect a public free-tier demo from being consumed by someone else's traffic, and `projects/04-ai-engineering/devmate/deploy/README.md:69` documents the trade-offs honestly: services sleep after idle, and free Postgres expires in 30 days per `projects/04-ai-engineering/devmate/deploy/README.md:74`. Cost engineering is deciding which trade-offs you accept on purpose.

Also count the AI-specific line items: GPU node pools idle at full price, embedding models re-embedded on every deploy waste both compute and vector-store writes, and log volume grows with every retrieval call an AI service logs. Instrument cost the way you instrument latency.

### 16. Putting It Together: A Production Manifest

One annotated example that carries sections 3, 5, 6, and 7. The `image` is pinned by digest, both probes exist, requests and limits are both set, and `runAsNonRoot` is set at pod level so it covers every container:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devmate-api
  namespace: devmate            # explicit target, never the context's default
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }   # capacity never dips
  selector:
    matchLabels: { app: devmate-api }
  template:
    metadata:
      labels: { app: devmate-api }
    spec:
      securityContext:
        runAsNonRoot: true      # applies to every container below
        fsGroup: 10001
      containers:
        - name: devmate-api
          image: ghcr.io/example/devmate-api@sha256:2c797b45f2d0b8e1
          ports: [{ containerPort: 8000 }]
          resources:
            requests: { cpu: 250m, memory: 512Mi }   # HPA denominator, scheduler input
            limits:   { cpu: "1",   memory: 1Gi }    # blast radius
          startupProbe:          # holds off the other probes while the model loads
            httpGet: { path: /health, port: 8000 }
            failureThreshold: 30
            periodSeconds: 10
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            periodSeconds: 15
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
            periodSeconds: 10
```

Run it through `projects/06-devops/deployment/exercises/01-deployment-strategies.py` before you trust it: the eight rules in that exercise are the eight cheapest mistakes to catch statically.

---

## Common Mistakes to Avoid

### 1. Using Liveness as a Startup Check

```yaml
# ❌ BAD: slow boots get killed into CrashLoopBackOff
livenessProbe:
  httpGet: { path: /health, port: 8000 }
  initialDelaySeconds: 5

# ✅ GOOD: gate startup explicitly, then let liveness guard steady state
startupProbe:
  httpGet: { path: /health, port: 8000 }
  periodSeconds: 10
  failureThreshold: 30
```

### 2. Deploying a Mutable Tag

```yaml
# ❌ BAD: restarts can pull different code; rollback restores nothing
image: ghcr.io/org/auth-service:latest

# ✅ GOOD: digest for production, or at minimum an immutable version tag
image: ghcr.io/org/auth-service:v1.5.0@sha256:9f2c1a4b...
```

### 3. Letting the HPA Divide by a Fantasy

```yaml
# ❌ BAD: target is 70% of 10m, so the HPA scales long after the pods are saturated
resources:
  requests: { cpu: 10m }
  limits:   { cpu: "4" }

# ✅ GOOD: requests reflect real usage, so the utilization math means something
resources:
  requests: { cpu: 250m, memory: 512Mi }
  limits:   { cpu: "1",   memory: 1Gi }
```

### 4. Switching Traffic Before the Schema Is Compatible

```yaml
# ❌ BAD: green writes a new column shape; the rollback to blue cannot read it
#    Fix with expand-then-contract: additive migration first, code that reads
#    both shapes second, destructive migration in a later release.
```

### 5. Treating Base64 as Encryption

```bash
# ❌ BAD: kubectl create secret generic db --from-literal=password=...
#         anyone who can read secrets in the namespace owns the password

# ✅ GOOD: sealed secrets committed to Git, decrypted only inside the cluster
kubeseal --format=yaml < db-secret.yaml > db-sealed.yaml
kubectl apply -f db-sealed.yaml
```

### 6. Rolling Back Without History or Headroom

```yaml
# ❌ BAD: revisionHistoryLimit 0 deletes the ReplicaSets you would undo to,
#        and maxUnavailable: 1 with replicas: 1 means a rollback has downtime
revisionHistoryLimit: 0

# ✅ GOOD: keep revisions, and keep capacity during the swap
revisionHistoryLimit: 10
strategy:
  rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
```

---

## Best Practices

1. **Promote one immutable digest** through every environment; never rebuild between staging and production
2. **Default to rolling updates** with `maxSurge: 1, maxUnavailable: 0` unless state forces recreate
3. **Choose the workload object by state**: Deployment for stateless, StatefulSet for identity and storage
4. **Give every service three probes**: startup for boot, readiness for traffic, liveness for wedged processes
5. **Set requests and limits on every container**, sized from measured usage, not from guesswork
6. **Never point liveness at a downstream dependency**; restart the pod only when the pod itself is broken
7. **Pin images by digest in production** and keep `revisionHistoryLimit` above zero
8. **Gate production on a human or a smoke-test gate**, while staging auto-deploys from main
9. **Deploy with GitOps where possible** so Git history is the audit log and drift is reverted
10. **Derive alerts from SLOs and error budgets** instead of round-number thresholds
11. **Encrypt secrets before they reach Git**; plain Secrets are for development only
12. **Write down RTO and RPO per component**, then prove them with a scheduled restore drill

---

## Practice Exercises

### Exercise 1: Choose a Strategy and Defend It
Take three services: a stateless API, a Postgres database, and a batch embedding job. Pick a strategy for each and write one paragraph justifying the choice against downtime, cost, and rollback speed. Then state what would change your mind.

### Exercise 2: Read the Rollout Clock
For a Deployment with `maxUnavailable: 0`, `minReadySeconds: 10`, and a readiness probe with `periodSeconds: 5`, compute how long a rollout takes for 6 replicas if each new pod becomes ready in 20 seconds. Show the arithmetic.

### Exercise 3: Convert a Threshold into an SLO
Pick one service and write an SLO (indicator, target, window), its error budget in minutes, and one burn-rate alert expression for the fast and slow burn cases. Explain why the p95 latency alert you would have written first is weaker.

### Exercise 4: Static-Review a Manifest
Write the Deployment from section 16 from scratch, then run `python exercises/01-deployment-strategies.py path/to/manifest.yaml` against it. Break it deliberately (drop the namespace, use `:latest`, delete the requests block) and confirm each rule fires before fixing it.

### Exercise 5: Rehearse a Rollback
In any cluster you control (kind, minikube, or a managed cluster), deploy v1, roll to v2 with `kubectl set image`, watch `kubectl rollout status`, then `kubectl rollout undo`. Record the wall-clock time from undo to fully ready, and identify which part of it is the readiness probe.

---

## Summary

Deployment strategy is a risk decision expressed as configuration: how much downtime you accept, how much capacity you double, and how fast you can reverse. The durable takeaways:

1. **The strategy is chosen, not defaulted.** Rolling for stateless, recreate for stateful writers, blue-green when you need a single-instant switch, canary when metrics should decide.
2. **One artifact, promoted unchanged.** Everything downstream (testing, rollback, audit) depends on the digest not changing between environments.
3. **Probes encode three different questions.** Startup asks if boot finished, readiness asks if traffic should flow, liveness asks if the process is worth keeping alive. Getting them backwards produces restart storms.
4. **Requests are a promise to the scheduler and to the HPA; limits are a blast radius.** Both together decide your QoS class and who gets evicted first.
5. **Rollback is a feature you can delete**: mutable tags, zero revision history, or a 90-second readiness gate each silently disable it.
6. **Observability without an SLO is dashboards without a decision rule.** Error budgets turn "should we ship?" into arithmetic.
7. **Backups are hypotheses until restored.** RTO and RPO become real only when a drill measures them.

**Next lecture:** CI/CD with GitHub Actions (`projects/06-devops/ci-cd/`), where the image built in the Docker track gets tested, scanned, promoted through these tiers, and wired to the deploy steps described here.
