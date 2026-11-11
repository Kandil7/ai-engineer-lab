# Data Engineering 22: Airflow Security and Platform

> **Pinned reference:** Apache Airflow 3.4.0 stable documentation
> (<https://airflow.apache.org/docs/apache-airflow/stable/index.html>). Concepts are
> Airflow's; the through-line is this repo's DevMate pipeline.

## Topic Overview

Topic 20 covered execution: executors, pools, retries, deployment shape. This lecture
covers the platform layer that keeps the scheduler safe and operable in production:
the security model (auth manager, RBAC, multi-team), connections and secrets
backends, lineage, listeners, plugins and the plugin manager, object storage,
task and asset state stores, installation, the web UI, best practices,
troubleshooting, and release policies.

The through-line is DevMate's public deployment (milestone A4). Once the ingest loop
runs on a public URL, the questions change from "does it run" to "who can trigger
it, where do the credentials live, how do we know when it fails, and how do we
upgrade without breaking it".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the Airflow auth model and when to use multi-team mode.
2. Move credentials out of the metadata database into a secrets backend.
3. Add lineage and listeners for auditability.
4. Decide when a plugin is warranted and how it is loaded.
5. Use object storage and the task/asset state stores correctly.
6. Install and upgrade Airflow without breaking the deployment.
7. Apply the documented best practices and troubleshoot common failures.

## Prerequisites

- Data Engineering 19, 20, and 21.
- DevOps Docker basics for the deployment sections.

---

## 1. Security Model

### Auth manager

Airflow 3 uses a pluggable auth manager. The default provides RBAC over Dags, task
instances, connections, and variables. Roles are composable; custom roles can be
defined for least-privilege access (e.g. "can trigger the DevMate Dag, nothing else").

### Multi-team

Multi-team mode scopes resources per team: separate Dag bundles, separate pools,
separate executor configuration, and asset-event filtering by producer team. Use it
when distinct teams share one Airflow instance but must not see or exhaust each
other's resources. For a single-team lab, it is overhead; for a shared platform, it
is the boundary that makes sharing safe.

### The Dag-file trust boundary

Dag files execute arbitrary Python with the scheduler's privileges. Write access to
the Dag bundle is production access: gate it like a deploy, review it like code, and
never let it be edited from the UI in production.

## 2. Secrets and Connections

### Connections at rest

Connections encrypt secrets in the metadata database. That is adequate for
development and small deployments, and it is not adequate for regulated environments
or for teams where the database is shared.

### Secrets backends

A secrets backend (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) moves
credentials out of the metadata database entirely. Tasks resolve connections through
the backend at runtime; rotation and auditing happen in the backend, not in Airflow.
The migration is: configure the backend, create the connections there, remove them
from the database, verify with a test task.

### The rule

No secret in a Dag file, no secret in an environment variable baked into an image,
no secret in a config file committed to git. Connections and secrets backends are the
only two sanctioned paths.

## 3. Lineage and Listeners

### Lineage

Airflow collects lineage metadata for tasks that declare inlets and outlets. It can
be limited (collected lineage only) to control volume. Lineage is what answers "which
Dag produced this table, and from what inputs" months later.

### Listeners

Listeners hook lifecycle events: DagRun state changes, task instance state changes,
asset events, Dag import errors. They are the integration point for audit logs,
metrics, and notification systems. A listener for Dag import errors is the cheapest
way to catch a broken Dag file before the scheduler does.

### When to use which

Lineage is for data provenance across systems; listeners are for operational events
inside Airflow. Use both: lineage for "what data", listeners for "what happened".

## 4. Plugins

### What plugins are for

Plugins extend Airflow with operators, hooks, executors, UI views, and translations.
They are the supported extension mechanism, as opposed to monkey-patching internals.

### Loading and lifecycle

Plugins are discovered from the plugins folder or installed as Python packages. They
reload according to the configured policy. UI plugins can add views, actions, and
translations, and can be scoped to specific Dags and tasks.

### The decision

Write a plugin when the capability is reusable across Dags and teams. Inline a helper
in a Dag when it is one-off. Airflow 3's public interface is the contract to build
against; internals change between releases.

## 5. Object Storage and State Stores

### Object storage

Airflow's object storage abstraction provides a path API over cloud object stores
(S3, GCS, Azure), with copy/move and integration hooks. It is how tasks read and
write large artifacts without embedding SDK calls, and it is the sanctioned path for
large data between tasks (topic 19's rule).

### Task and asset state stores

Task and asset state stores provide shared, durable state for tasks and assets:
access patterns, sync versus deferrable usage, mapped tasks, and garbage collection.
They are configured separately, with their own backends and cleanup policies.
Use them for coordination state that must survive a worker restart, not for passing
data (that is object storage or XCom).

## 6. Installation and Upgrades

### Installation

Airflow is installed with constraints: a constraints file pins transitive
dependencies for a given Python and Airflow version. Installing without constraints
is the most common way to get an unimportable Airflow.

### Upgrading

Live upgrades are supported for moving between versions. Database migrations run on
upgrade and must be planned. Dag bundles and the public interface are the parts
that survive upgrades; code depending on internals does not.

### Release policies

Airflow follows defined release policies and publishes release notes. Pin the
version in the constraints file and in the deployment image; never track "latest"
in production.

## 7. UI and Operations

### UI overview

The web UI provides graph, grid, overview, and task-log views, plus admin screens for
connections, variables, pools, and users. It is the primary debugging surface; task
logs per attempt are the first thing to read on a failure.

### Best practices

The documented best practices cover Dag authoring, testing, deployment, and
performance. The recurring themes: keep Dags idempotent, test task functions
directly, use pools, set timeouts, and avoid top-level execution in Dag files.

### Troubleshooting

Common failure modes: import errors (Dag never appears), scheduler not picking up
Dags (parse errors, file permissions), tasks stuck queued (no worker capacity, pool
exhaustion), and timezone confusion. Each has a documented diagnostic path; the
scheduler heartbeat and the task log are the two signals to check first.

## 8. Observability Recap

### What to monitor

Scheduler heartbeat, task failure rate, pool occupancy, queue depth, triggerer health,
and SLA misses. Each needs a threshold and an owner. Callbacks (`on_failure_callback`)
route failures to notifications. Metrics ship via statsd or Prometheus; logs ship
centrally so a dead worker's logs survive.

### The DevMate gate

The eval gate (Hit@5 >= 1.0) is a task that fails the run on regression. A failing
task is the simplest, most reliable alert: it blocks downstream steps and surfaces in
the UI and in callbacks without extra plumbing.

## Real-World Application

- DevMate on a public URL: RBAC so only the owner can trigger, a secrets backend
  for the Qdrant and LLM credentials, lineage on the ingest task, a listener that
  pages on Dag import errors, and pool limits carried over from topic 20.
- Plugins only if a custom operator or UI view is genuinely needed; otherwise inline
  helpers.
- Pinned Airflow version in the image and constraints file; upgrades rehearsed
  against a staging instance before production.
- Object storage for the passages and index artifacts; task state store only for
  coordination state that must survive a worker restart.

## Common Mistakes

1. **Secrets in Dag files or images.** Connections and secrets backends exist for
   this; a leaked Dag file must carry no credentials.
2. **Treating Dag-file write access as documentation access.** It is production
   access.
3. **No listeners for import errors.** A broken Dag fails silently until the next
   scheduled run is missed.
4. **Tracking "latest" Airflow in production.** Pin the version and the constraints.
5. **Storing data in the task state store.** It is coordination state; data goes
   through object storage or XCom.
6. **Skipping the staging upgrade rehearsal.** Migrations are deploy-time work.

## Key Takeaways

1. Auth manager plus multi-team scopes access and resources per team.
2. Secrets backends move credentials out of the metadata database.
3. Listeners catch operational events; lineage captures data provenance.
4. Plugins are the supported extension path; build against the public interface.
5. Object storage carries data; state stores carry coordination state.
6. Pin versions, use constraints, and rehearse upgrades.

## Self-Check Questions

1. When is multi-team mode worth the overhead?
2. Why is a secrets backend better than encrypted connections in the database?
3. What is the difference between lineage and a listener?
4. When should you write a plugin versus an inline helper?
5. What belongs in object storage versus the task state store?
6. Why must Airflow be installed with a constraints file?

## Further Reading / Connections

- Data Engineering 20 (execution and operations) — executors, pools, deployment shape.
- Data Engineering 21 (advanced authoring) — the authoring surface this secures.
- Airflow 3.4 docs: Security (Auth manager, Multi-Team), Administration and
  Deployment (Production Deployment, Logging & Monitoring, Plugins, Object Storage,
  Task and Asset State Store), Best Practices, FAQ, Troubleshooting, Release Policies,
  and Installation.
