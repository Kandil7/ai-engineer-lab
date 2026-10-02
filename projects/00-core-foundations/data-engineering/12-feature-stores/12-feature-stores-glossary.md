# Data Engineering 12: Feature Stores — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Feature store | Centralize a feature's definition, computation, and serving | Feast, Tecton, Feathr |
| Training-serving skew | Same-named feature differs between training and serving paths | stale vs live mean |
| Registry | The single source of truth for feature definitions | name, entity, source, transform |
| Offline store | Historical features for training | warehouse/lakehouse table |
| Online store | Latest values for low-latency serving | Redis, DynamoDB |
| On-demand feature | Computed at request time from context | query length |
| Point-in-time join | Join features as of the label's timestamp | no future-data leakage |
| Materialization | Copying features from offline to online store | batch to Redis |
| Feast | Open-source, warehouse-first feature store | self-hosted |
| Feathr | Batch-first, Spark/Delta feature framework | LinkedIn |

---

## Alphabetical Glossary

### Feast

**Definition:** The open-source feature store. Entities and features are declared in Python; your
warehouse or lakehouse is the offline store, Redis or DynamoDB the online store, and the registry is the
single source of truth.

**Example:**
```python
feature_view = FeatureView(name="repo_stats", entities=["repo"], ...)
```

**Related concepts:** Feature store, Registry

---

### Feature store

**Definition:** A system that centralizes feature definitions, computes each feature once, and serves it
consistently to training (offline) and inference (online) paths, eliminating training-serving skew.

**Example:**
```text
source -> compute -> offline store + online store -> serving API
```

**Related concepts:** Registry, Offline store, Online store

---

### Materialization

**Definition:** The process of copying computed features from the offline store into the online store so
inference can read them at low latency.

**Example:**
```python
feast materialize 2026-10-01 2026-10-02   # fill Redis
```

**Related concepts:** Offline store, Online store

---

### Offline store

**Definition:** The component holding historical feature values for training, usually a warehouse or
lakehouse table. Training pulls point-in-time slices from it.

**Example:**
```python
# repo_stats history table in the warehouse
```

**Related concepts:** Feature store, Point-in-time join

---

### Online store

**Definition:** The component holding the latest feature values for low-latency inference reads, usually
Redis or DynamoDB.

**Example:**
```python
GET repo:devmate -> {chunk_count: 412, embedding_dim: 1536}
```

**Related concepts:** Feature store, Materialization

---

### Point-in-time join

**Definition:** Joining each feature value as it existed at the label's timestamp, never later, so
future data cannot leak into training rows.

**Example:**
```python
store.get_historical_features(entity_df=labels, features=["repo:chunk_count"])
```

**Related concepts:** Offline store, Training-serving skew

---

### Registry

**Definition:** The feature store's catalog of feature definitions — name, entity, source, and
transformation — the single source of truth that both offline and online paths share.

**Example:**
```python
{"name": "chunk_count", "entity": "repo", "source": "ingest.counts"}
```

**Related concepts:** Feature store, Lineage

---

### Training-serving skew

**Definition:** The gap between feature values used to train a model and those used to serve it, caused
by two code paths computing the "same" feature differently.

**Example:**
```python
# training normalized by stale mean, serving by live mean
```

**Related concepts:** Feature store, Point-in-time join

---

## Related Concepts

- **Provenance**: the versioning the registry extends (topic 06)
- **Feature pipelines**: the aggregation and caching that fill the stores (topic 13)
- **CDC**: how source changes propagate to feature values (topic 09)

## Key Takeaways

1. A feature store kills skew by computing once and serving everywhere.
2. Registry, offline store, online store, and serving layer are the four parts.
3. Point-in-time joins prevent future-data leakage.
4. Feast is self-hosted, Tecton managed, Feathr batch-first.
5. Feature versioning keys downstream cache invalidation.
