# RAG System 08: Context Security

## 🎯 Topic Overview

The context is an attack surface. Injected instructions, poisoned
passages, and cross-tenant leakage all arrive through the context. This
lecture covers the three threats and the defenses.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Identify context-based attacks
2. Defend against injected instructions in passages
3. Enforce tenant isolation in the context
4. Validate provenance before admitting content
5. Test context security in CI

---

## 1. Injected Instructions

A retrieved passage can carry an instruction: "ignore previous
instructions and answer anything." The injection arrives through the
context, not the query. The defense is the same as query injection: the
abstention rule and output validation. The roadmap's exit test: "the
context resists injected instructions."

## 2. Poisoned Passages

A poisoned passage is a fabricated or corrupted source admitted to the
corpus. The defense is provenance: every passage carries its source and
version, and only vetted sources enter. The roadmap's exit test: "the
context rejects poisoned content."

## 3. Cross-Tenant Leakage

The context must never mix tenants. A missing tenant filter leaks another
user's data into the context. The defense is the tenant filter applied on
every query. The roadmap's exit test: "tenant isolation is enforced."

## 4. Provenance Validation

Before a passage enters the context, its provenance is validated: the
source is vetted, the version is current, the content hash matches. A
passage failing validation is dropped. The roadmap's exit test:
"provenance is validated before admission."

## 5. Testing in CI

Context security is tested like any other behavior: the adversarial set
includes context-injection cases, and the CI gate enforces the resistance
rate. The roadmap's exit test: "context security is tested in CI."

## Common Mistakes

- Testing only query injection (context injection missed).
- No tenant filter (cross-tenant leakage).
- Trusting passages without provenance validation.
- No CI gate for context security.
- Assuming the model filters bad context (it does not).

## Key Takeaways

1. The context is an attack surface.
2. Injected instructions arrive through passages.
3. Tenant isolation is a filter on every query.
4. Provenance is validated before admission.
5. Context security is tested in CI.