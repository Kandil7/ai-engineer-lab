# Prompt Engineering 05: End-User IDs — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| End-user ID | The identity in the prompt | metadata, not content |
| ID injection | Instructions smuggled in the ID | format validation |
| Per-user isolation | Each user's data is separate | tenant filter |
| Format validation | Strict regex on the ID | [a-zA-Z0-9-]{1,64} |
| Per-user logging | Queries logged with the ID | audit trail |
| Rate limiting | Per-user request bounds | abuse prevention |
| Audit trail | The record of who asked what | compliance |

---

## Alphabetical Glossary

### Audit trail

**Definition:** The record of who asked what. Enabled by per-user logging.

**Example:**
```python
# log(user_id, query, answer, timestamp)
```

**Related concepts:** Per-user logging

---

### End-user ID

**Definition:** The identity carried in the prompt. Metadata, not content —
it must never be interpreted as an instruction.

**Example:**
```python
f"User ID: {user_id}. Follow all instructions below."
```

**Related concepts:** ID injection

---

### Format validation

**Definition:** A strict regex check on the ID before use. Prevents
malicious IDs from passing.

**Example:**
```python
re.fullmatch(r"[a-zA-Z0-9-]{1,64}", user_id)
```

**Related concepts:** ID injection

---

### ID injection

**Definition:** Instructions smuggled into the user ID field. Prevented by
format validation and never interpolating the ID as content.

**Example:**
```python
# "x. Ignore all instructions." -> rejected by format validation
```

**Related concepts:** Format validation

---

### Per-user isolation

**Definition:** Each user's context and memory are separate. Mirrors
tenant isolation.

**Example:**
```python
# user A's prompt never contains user B's data
```

**Related concepts:** End-user ID

---

### Per-user logging

**Definition:** Logging each user's queries and answers with the ID.
Enables audit, abuse detection, and rate limiting.

**Example:**
```python
log(user_id, query, answer)
```

**Related concepts:** Audit trail

---

## Related Concepts

- **Prompt structure**: the ID is part of the system prompt (topic 01)
- **Context security**: the same isolation principle (rag-system 08)
- **Rate limiting**: per-user limits (redis-cache 03)

## Key Takeaways

1. The ID is metadata, not content.
2. Per-user isolation mirrors tenant isolation.
3. ID injection is prevented by format validation.
4. Per-user logging enables audit and rate limiting.
5. ID handling is tested in CI.