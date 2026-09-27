# Component Contracts Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Contract | Documented, tested agreement between producer and consumer |
| Producer | Component that emits data or events |
| Consumer | Component that reads data or events |
| Shape | The fields/types/nullability of a payload (wire format) |
| Semantics | What each field *means*, documented in the contract |
| Invariant | Condition that must always hold over valid payloads |
| Version | Contract revision; minor = compatible, major = breaking |
| Compatible change | Change consumers can ignore (e.g. add optional field) |
| Breaking change | Change that breaks existing consumers immediately |
| Needs-migration change | Change requiring producer/consumer coordination |
| Add-optional | Compatible schema addition |
| Add-required | Schema addition needing the 4-step migration |
| Remove-field | Breaking change; deprecate first |
| Dual-write | Writing old and new field during a rename migration |
| Deprecation window | Version span where old field still works |
| Emit-default | Producer sends new field with default before requiring it |
| Backfill | Filling a new field for existing records |
| Contract test | CI test asserting payload satisfies the contract |
| Producer contract test | Proves what the producer emits is valid |
| Consumer contract test | Proves consumer tolerates supported versions |
| Schema drift | Producer and consumer disagree on shape/meaning |
| Semantic drift | Same shape, different meaning (page 0 vs 1-based) |
| Rolling upgrade | Deploying producer/consumer at different times safely |
| Shared contract artifact | Versioned file both teams reference |
| JSON Schema | Standard for expressing a data contract |
| Wire format | On-the-wire shape, ignoring meaning |
| Classify-change | Mechanically label a change compatible/breaking/migrating |
| Invariant violation | Payload breaks an always-true rule; must name the rule |
| Verbatim NFC | Normalized storage form; never folded in the record |
| Lineage key | `source_ref` tying records to their source (an invariant) |

---

## Detailed Definitions

### Contract (four parts)
Shape, semantics, invariants, and version. Shape alone is a wire format; the contract makes meaning and rules explicit so two codebases cannot quietly disagree.

### Compatibility classes
Compatible (consumers ignore), needs-migration (coordination required), breaking (consumers break now). Adding fields is safe only if optional at first; removals and renames are breaking.

### Migration path for required fields
Emit-with-default → consumers read when present → backfill history → tighten to required. At each step both old and new versions must work (the rolling-upgrade principle).

### Contract tests
Producer-side: emitted payloads satisfy the contract. Consumer-side: the consumer tolerates every supported version. Both run in CI; the producer-side version-boundary test proves the boundary is real.

### Semantics and invariants
Field meaning (page is 1-based physical page in that edition) and always-true rules (`source_ref == f"{book}/p{page}"`). Invariant failures must name the rule and the offending values.

### Schema vs semantic drift
Schema drift: shape mismatch (missing field). Semantic drift: same shape, different meaning (PDF page vs edition page). Only documented semantics catch the second.

### Shared contract artifacts
Versioned JSON/JSON Schema/Protobuf in a repo both teams read; reviewed like code; semver where minor = compatible and major = breaking; deprecations live at least one full version.

### Rolling upgrade
Producer and consumer deploy at different times. Contracts make this safe: transitional states are defined, and contract tests assert each state is valid.
