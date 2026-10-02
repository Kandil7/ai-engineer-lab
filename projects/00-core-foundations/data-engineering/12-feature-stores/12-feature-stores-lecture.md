# Data Engineering 12: Feature Stores

## Topic Overview

The same feature, computed twice, by two different code paths, is the classic source of
training-serving skew. A feature store exists to kill that skew: define a feature once, compute it once,
and serve it consistently to both the training path (offline, high-volume) and the inference path
(online, low-latency). Feast, Tecton, and Feathr are three implementations of this idea at different
levels of managedness.

The core components are always the same. A registry records feature definitions and their metadata. An
offline store holds historical features for training. An online store holds the latest values for
low-latency serving. The critical guarantee is consistency: the value served online at inference must be
computed by the same definition as the value used in training, otherwise the model is trained on one
definition and asked to predict from another.

For our systems this is concrete. DevMate's retrieval features — a repository's chunk count, its
embedding dimension, its doc-type distribution — could be recomputed ad hoc in both the ingest path and
the ask path, drifting apart. A feature store centralizes them. Athar's passage features, keyed by
`book_id`, follow the same pattern.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why training-serving skew happens and how a feature store prevents it.
2. Name the four components of a feature store and their roles.
3. Distinguish offline, online, and on-demand feature computation.
4. Compare Feast, Tecton, and Feathr along managedness and streaming support.
5. Explain point-in-time correctness and why naive materialization leaks data.
6. Map a DevMate retrieval feature through registry, offline, and online stores.
7. Connect feature versioning to the provenance discipline of earlier lectures.

## Prerequisites

- Data Engineering 08 (batch vs streaming) for offline versus online computation.
- Data Engineering 09 (ELT and CDC) for how changes propagate to features.

---

## 1. The Skew Problem

### Training-serving skew

Skew is the gap between the feature values used to train a model and the values used to serve it. It
arises when the two paths compute the "same" feature differently: one normalizes with a stale mean, one
with a live mean; one uses a rolling window, one a fixed snapshot. The model is trained on one
distribution and scored against another, so its metrics lie.

### Why it is subtle

Skew is invisible until a model misbehaves, because both paths produce a number with the same name. The
feature name is the same; the definition drifted. Detecting it after the fact is hard, which is why the
fix is structural: one definition, one computation, one source of truth.

### The single-source rule

A feature store enforces the single-source rule by construction. The definition lives in the registry;
the store materializes it once; both serving and training read the same materialized value. The
definition and the value travel together, so drift is impossible by design rather than by vigilance.

## 2. The Four Components

### Registry

The registry holds the definitions: name, entity, data source, transformation, and metadata. It is the
catalog of what a feature means, independent of any single computed value.

### Offline store

The offline store holds historical feature values for training, usually in a warehouse or lakehouse
table. Training pulls a point-in-time slice of features for each entity.

### Online store

The online store holds the latest values for low-latency serving, usually Redis or DynamoDB. Inference
reads a feature vector for an entity in single-digit milliseconds.

### Serving layer

The serving layer is the API that reads the online store and, optionally, computes on-demand features at
request time. It is the boundary between the feature store and the model.

### How they compose

```text
feature source ──> compute ──> offline store (training) ─┐
                       └──────> online store (serving) ──┴──> serving API ──> model
registry: the single definition both sides share
```

## 3. Offline, Online, On-Demand

### Offline computation

Offline features are computed in batch from the full history: a corpus statistic, a weekly aggregate, a
precomputed embedding. They are materialized into the offline store and joined into the training set.

### Online computation

Online features are computed incrementally as events arrive, or refreshed from a scheduled job, and
stored in the online store for fast reads. A rolling count of recent requests is online.

### On-demand (request-time) computation

On-demand features are computed at request time from request context — the current query's length, the
user's session id — not stored in advance. They trade a little latency for always-fresh values.

### The consistency rule

The rule that binds them: the same named feature must have the same definition in all three. Feast
expresses this by storing the definition in the registry and generating consistent logic for offline,
online, and on-demand paths from that one source.

## 4. Feast, Tecton, Feathr

### Feast

Feast is the open-source feature store. You declare entities and features in Python; it uses your
warehouse or lakehouse as the offline store and Redis or DynamoDB as the online store, and it
materializes features between them. The registry is the single source of truth. It is the right choice
when you want self-hosted control and already have a warehouse.

### Tecton

Tecton is the managed platform. It adds a declarative spec for batch, streaming, and real-time features,
built-in transformation (Spark, Snowflake), and fully managed online serving. It is the low-ops choice
when feature velocity is high and you want streaming features without running the infrastructure.

### Feathr

Feathr (LinkedIn) is batch-first and deeply tied to the Spark/Delta ecosystem. It defines features as
transformations over a source and materializes them into an offline store for training; online serving
requires an external store. It is the choice when your stack is already Spark and Delta and you need
batch features for training more than low-latency serving.

### The choosing rule

Self-hosted and warehouse-first → Feast. Managed and streaming-first → Tecton. Spark/Delta batch-first →
Feathr. The choice is about managedness, streaming needs, and where your data already lives.

## 5. Point-in-Time Correctness

### The leakage trap

The naive way to build a training set is to join features "as of now." That leaks: a feature value that
depends on future data — the outcome you are predicting, or a label's future state — ends up in the
training row. The model memorizes the future and over-performs in training, then collapses in
production.

### Point-in-time joins

Point-in-time correctness means joining each feature as it existed at the timestamp the label was
created, never later. The feature store keeps feature history with timestamps and joins by
`(entity, timestamp)`, so a training row only sees data available at that moment.

### The code shape

```python
# join features as of each label's timestamp, not as of now
training = feature_store.get_historical_features(
    entity_df=labels,  # entity + label_timestamp
    features=["repo:chunk_count"],
)
```

### Why the store helps

A feature store makes point-in-time joins a built-in operation, which is exactly the kind of correctness
that is easy to get wrong by hand and nearly free when the store does it. It is the feature-store
analogue of the re-run safety this curriculum keeps returning to.

## 6. Feature Versioning and Lineage

### Versioning a feature

A feature's definition changes when its source, window, or transformation changes. The registry records a
version for each definition, so a model can pin "chunk_count v2" and keep training against it even after
v3 ships. This is the same versioning discipline as Data Engineering 06, applied to features.

### Lineage of a feature

Lineage tracks where a feature came from: source column, transformation, and the entities it joins on.
When a source changes, lineage says which features are affected and therefore which models must retrain.
This is the impact-analysis idea that Data Engineering 14 develops fully.

### The link to the cache key

The feature version appears in the cache key of downstream artifacts, exactly as `source_version` did in
Data Engineering 06. A feature-version bump invalidates the cached model inputs consistently, closing the
loop between source change and serving refresh.

## 7. The DevMate Mapping

### The retrieval features

DevMate's retrieval layer can be framed as a feature store: entity `repo`, features `chunk_count`,
`embedding_dim`, `doc_type_ratio`, and `recency`. The ingest path materializes them offline (for any
offline eval) and online (for the ask path), from the same registry definition.

### The consistency payoff

Because the ask path and any offline eval read the same materialized feature, a metric computed offline
agrees with the live behavior. That is the concrete value: retrieval features stop drifting between
ingest and query.

### The pragmatic floor

A full feature store may be more than DevMate needs at its scale. The pragmatic floor is the discipline:
one definition, one computation, served to both paths, with a version in the cache key. Adopting the
discipline without the infrastructure buys most of the correctness at none of the ops cost.

## Real-World Application

- Declaring the Athar passage features (`book_id`, `chunk_count`, `embedding_dim`) once in a Feast
  registry, with the corpus as the offline source.
- Materializing the latest values into Redis for the online ask path, so query-time features match
  ingest-time features.
- Building a point-in-time training set for a DevMate relevance model, joining features as of each
  label's timestamp to avoid leakage.
- Pinning a feature version in the cache key so a redefinition invalidates downstream artifacts.

## Common Mistakes

1. **Two code paths for one feature.** Training-serving skew, invisible until production.
2. **Joining features "as of now".** Future data leaks into training rows.
3. **No registry.** Features exist only as scattered code, unversioned and unlineaged.
4. **Recomputing from raw on every request.** Latency that a materialized online store avoids.
5. **Ignoring feature versions.** Models silently train against a changed definition.
6. **Over-engineering.** Running Feast for one repository's handful of features.

## Key Takeaways

1. Training-serving skew comes from two paths for one feature; the store's single source kills it.
2. The four components are registry, offline store, online store, and serving layer.
3. Offline, online, and on-demand features share one definition from the registry.
4. Point-in-time joins prevent the future-data leakage that naive joins cause.
5. Feature versioning and lineage extend provenance to features, keying cache invalidation.

## Self-Check Questions

1. Why is training-serving skew hard to detect, and how does a feature store prevent it?
2. What are the four components, and which one is the single source of truth?
3. Why does a naive "as of now" join leak future data into training?
4. How do Feast, Tecton, and Feathr differ, and what question decides among them?
5. How does feature versioning connect to the cache-key discipline of earlier lectures?

## Further Reading / Connections

- Data Engineering 08 (batch vs streaming) — offline versus online computation.
- Data Engineering 09 (ELT and CDC) — how changes propagate to feature values.
- Data Engineering 06 (provenance) — the versioning the registry extends.
- Data Engineering 13 (feature pipelines) — the aggregation and caching that fill the stores.
- `projects/04-ai-engineering/devmate/src/devmate/retrieve/` — the retrieval features this maps to.
