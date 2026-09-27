# Athar Lab — Learning Copy

The first building block of the Athar roadmap: a separate learning copy that
grows into the real Athar system. Stage 1 exit test — a CLI that reads
Arabic page files and emits JSONL without ever losing `book_id` or `page`.

## Contracts

- `SourceLocation` — `book_id`, `page`, `source_version`, optional path.
  `book_id` must be non-empty; `page` must be >= 1.
- `Document` — stable book identity: `book_id`, `title`, `source_version`.
- `Passage` — one retrievable unit with **two texts**: `original` (verbatim,
  for display and citation) and `searchable` (normalized, for matching).
  The two-text discipline is enforced from day one.

## Run

```bash
# read 10 Arabic page files, emit JSONL
python cli.py sample_pages b1 v1 -o out.jsonl

# run the exit tests
python -m pytest tests/ -q
```

## Exit test (stage 1)

- Handles a valid file and a corrupted one (unparseable filename raises).
- Never loses Arabic (UTF-8 round trip asserted).
- Re-running produces identical output (deterministic).
- Every passage carries `book_id` and `page` — losing either is a bug.

## Next stages

Stage 2 packages this into a proper module (parser/normalizer/writer
separated). Stage 5 adds idempotent ETL with provenance. The real
Athar-Lab ingestion models are Shamela-specific and deeper; this copy stays
portable on purpose.