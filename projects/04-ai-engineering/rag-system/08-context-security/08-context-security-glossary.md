# RAG System 08: Context Security — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Context injection | An instruction smuggled in a passage | "ignore previous" |
| Poisoned passage | A fabricated or corrupted source | fake hadith |
| Cross-tenant leakage | Another tenant's data in the context | missing filter |
| Provenance validation | Checking source, version, content hash | before admission |
| Tenant filter | The correctness boundary on every query | always applied |
| Vetted source | An approved corpus source | provenance-trusted |
| Content hash | The passage's integrity check | SHA-256 |

---

## Alphabetical Glossary

### Content hash

**Definition:** The passage's integrity check — a hash of the content. A
mismatch means the passage was tampered with.

**Example:**
```python
sha256(passage_text) == recorded_hash
```

**Related concepts:** Provenance validation

---

### Context injection

**Definition:** An instruction smuggled into a retrieved passage that
tries to override the system prompt. Arrives through the context, not the
query.

**Example:**
```python
# a passage that says "ignore previous instructions"
```

**Related concepts:** Poisoned passage

---

### Cross-tenant leakage

**Definition:** Another tenant's data appearing in the context. Caused by
a missing tenant filter.

**Example:**
```python
# user A sees user B's passage in the context
```

**Related concepts:** Tenant filter

---

### Poisoned passage

**Definition:** A fabricated or corrupted source admitted to the corpus.
The defense is provenance.

**Example:**
```python
# a fabricated hadith in the corpus
```

**Related concepts:** Context injection, Provenance validation

---

### Provenance validation

**Definition:** Checking the source is vetted, the version is current, and
the content hash matches before a passage enters the context.

**Example:**
```python
if not validate_provenance(passage):
    drop(passage)
```

**Related concepts:** Content hash, Vetted source

---

### Tenant filter

**Definition:** The correctness boundary: a filter applied on every query
so a tenant's results never include another tenant's data.

**Example:**
```python
# every query carries the tenant filter
```

**Related concepts:** Cross-tenant leakage

---

### Vetted source

**Definition:** An approved corpus source. Only vetted sources enter the
corpus.

**Example:**
```python
# source in the approved list -> admitted
```

**Related concepts:** Provenance validation

---

## Related Concepts

- **Adversarial evaluation**: the attack set covers these threats (ai-evaluation 05)
- **Abstention**: the guard on injected instructions (topic 05)
- **Metadata filtering**: the tenant filter (qdrant-rag 04)

## Key Takeaways

1. The context is an attack surface.
2. Injected instructions arrive through passages.
3. Tenant isolation is a filter on every query.
4. Provenance is validated before admission.
5. Context security is tested in CI.