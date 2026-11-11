# Data Engineering 22: Airflow Security and Platform — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Auth manager | Pluggable authentication/authorization for Airflow | RBAC over Dags |
| RBAC | Role-based access control | trigger-only role |
| Multi-team | Per-team scoping of resources in one instance | separate pools per team |
| Secrets backend | External store for credentials (Vault, AWS SM) | rotate in Vault |
| Lineage | Data provenance across tasks and systems | table produced by Dag X |
| Listener | Hook on Airflow lifecycle events | page on import error |
| Plugin | Supported extension: operators, hooks, UI views | custom operator |
| Public interface | Documented extension contract for Airflow 3 | stable APIs |
| Object storage | Path API over cloud object stores | passages in S3 |
| Task state store | Durable coordination state for tasks | survives worker restart |
| Asset state store | Durable state for assets | partition progress |
| Constraints file | Pinned transitive deps for an Airflow version | `constraints-3.4.0.txt` |
| Live upgrade | Supported in-place version upgrade | with DB migrations |
| Release policy | Airflow's documented release cadence | pin, don't track latest |
| Callback | Hook on state change for notifications | `on_failure_callback` |

---

## Alphabetical Glossary

### Auth manager

**Definition:** Pluggable component handling authentication and authorization in
Airflow 3. The default provides RBAC over Dags, task instances, connections, and
variables.

**Example:**
```python
# custom role: can trigger devmate_ingest only
```

**Related concepts:** RBAC, Multi-team

---

### Callback

**Definition:** Hook invoked on task or Dag state change, used to route failures and
events to notifications.

**Example:**
```python
task = ingest.override(on_failure_callback=page_oncall)
```

**Related concepts:** Listener, Monitoring (topic 20)

---

### Constraints file

**Definition:** File pinning transitive dependencies for a specific Airflow and
Python version. Installing without it is the most common cause of an unimportable
Airflow.

**Example:**
```bash
pip install "apache-airflow==3.4.0" --constraint constraints-3.4.0.txt
```

**Related concepts:** Live upgrade, Release policy

---

### Lineage

**Definition:** Data provenance metadata collected for tasks declaring inlets and
outlets, answering which Dag produced a dataset and from what inputs.

**Example:**
```python
# lineage recorded for the ingest task's outlets
```

**Related concepts:** Listener, Asset (topic 21)

---

### Listener

**Definition:** Hook on Airflow lifecycle events (DagRun state, task instance state,
asset events, import errors). Integration point for audit, metrics, notifications.

**Example:**
```python
# listener pages on Dag import error
```

**Related concepts:** Callback, Lineage

---

### Live upgrade

**Definition:** Supported in-place upgrade between Airflow versions, including
database migrations that must be planned.

**Example:**
```bash
# rehearse migrations on staging first
```

**Related concepts:** Constraints file, Release policy

---

### Multi-team

**Definition:** Mode scoping resources per team: separate Dag bundles, pools, executor
config, and asset-event filtering. Overhead for one team, boundary for shared
platforms.

**Example:**
```python
# team A cannot exhaust team B's pool
```

**Related concepts:** Auth manager, RBAC

---

### Object storage

**Definition:** Airflow's path API over cloud object stores (S3, GCS, Azure) with
copy/move and integrations. The sanctioned path for large data between tasks.

**Example:**
```python
# passages written to s3://bucket/passages/
```

**Related concepts:** XCom (topic 19), Task state store

---

### Plugin

**Definition:** Supported extension mechanism for operators, hooks, executors, UI
views, and translations. Loaded from the plugins folder or as a Python package.

**Example:**
```python
# custom operator packaged as a plugin
```

**Related concepts:** Public interface, Best practices

---

### Public interface

**Definition:** Airflow 3's documented extension contract for operators, plugins, UI,
and executors. Build against it; internals change between releases.

**Example:**
```python
# depend on airflow.sdk, not internals
```

**Related concepts:** Plugin, Live upgrade

---

### RBAC

**Definition:** Role-based access control over Dags, task instances, connections,
and variables. Roles are composable for least privilege.

**Example:**
```python
# "can trigger devmate_ingest only"
```

**Related concepts:** Auth manager, Multi-team

---

### Release policy

**Definition:** Airflow's documented release cadence and versioning. Production pins
the version and constraints; tracking "latest" is unsafe.

**Example:**
```bash
# pin apache-airflow==3.4.0 in the image
```

**Related concepts:** Constraints file, Live upgrade

---

### Secrets backend

**Definition:** External credential store (Vault, AWS Secrets Manager, GCP Secret
Manager) that moves credentials out of the metadata database.

**Example:**
```python
# connection resolved from Vault at runtime
```

**Related concepts:** Connection (topic 19), Auth manager

---

### Task state store

**Definition:** Durable coordination state for tasks that survives a worker restart.
For coordination state, not data; data goes through object storage or XCom.

**Example:**
```python
# checkpoint survives worker crash
```

**Related concepts:** Object storage, Asset state store

---

## Related Concepts

- **Execution and operations** (topic 20): pools, executors, deployment shape.
- **Advanced authoring** (topic 21): the authoring surface this secures.
- **Idempotency** (topic 03): the property retries and backfills stand on.

## Key Takeaways

1. Auth manager plus multi-team scopes access and resources per team.
2. Secrets backends move credentials out of the metadata database.
3. Listeners catch operational events; lineage captures data provenance.
4. Plugins are the supported extension path; build against the public interface.
5. Object storage carries data; state stores carry coordination state.
6. Pin versions, use constraints, and rehearse upgrades.
