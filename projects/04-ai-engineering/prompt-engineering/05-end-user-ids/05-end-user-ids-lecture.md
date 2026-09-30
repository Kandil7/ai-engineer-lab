# Prompt Engineering 05: End-User IDs in Prompts

## 🎯 Topic Overview

Prompts that carry user identity need careful handling. The end-user ID
enables per-user isolation, rate limiting, and audit trails — but it is
also an injection vector. This lecture covers the ID, the isolation, and
the injection defense.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Include an end-user ID in the prompt safely
2. Enforce per-user isolation
3. Defend against ID injection
4. Log per-user activity
5. Test the ID handling

---

## 1. The End-User ID

The end-user ID identifies who is asking. It is used for rate limiting,
audit trails, and per-user context. The ID is metadata, not content — it
must never be interpreted as an instruction. The roadmap's exit test: "the
end-user ID is included safely."

```python
# The ID is metadata, not instruction
{"role": "system", "content": f"User ID: {user_id}. Follow all instructions below."}
```

## 2. Per-User Isolation

Each user's context and memory are isolated. User A's prompt must never
contain User B's data. The isolation is the same tenant filter as
retrieval. The roadmap's exit test: "per-user isolation is enforced."

## 3. ID Injection

An attacker can put instructions in the user ID: `"x. Ignore all
instructions."` The defense: the ID is validated against a strict format
and never interpolated as content. The roadmap's exit test: "ID injection
is prevented."

```python
# Validate the ID format before use
if not re.fullmatch(r"[a-zA-Z0-9-]{1,64}", user_id):
    reject("invalid user ID")
```

## 4. Per-User Logging

Each user's queries and answers are logged with the ID. The log enables
audit trails, abuse detection, and per-user rate limiting. The roadmap's
exit test: "per-user activity is logged."

## 5. Testing

The ID handling is tested: valid IDs pass, injected IDs are rejected, and
isolation holds. The tests are in CI. The roadmap's exit test: "ID
handling is tested."

## Common Mistakes

- Interpolating the ID as content (injection).
- No format validation (malicious IDs pass).
- No per-user isolation (cross-user leakage).
- No per-user logging (no audit trail).
- No tests for ID handling.

## Key Takeaways

1. The ID is metadata, not content.
2. Per-user isolation mirrors tenant isolation.
3. ID injection is prevented by format validation.
4. Per-user logging enables audit and rate limiting.
5. ID handling is tested in CI.