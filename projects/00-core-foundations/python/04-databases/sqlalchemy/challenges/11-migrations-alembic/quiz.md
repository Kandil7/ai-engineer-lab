# Challenge 11 — Quiz: Migrations and Schema Evolution

1. The safe order for adding a NOT NULL column is:
   - A) one ALTER  (B) expand, backfill, contract  (C) drop, recreate  (D) rename
2. An applied migration file should be:
   - A) edited freely  (B) immutable; write a follow-up  (C) deleted  (D) renamed
3. `downgrade()` exists because:
   - A) docs say so  (B) rollback must be possible  (C) tests need it  (D) style
4. A data migration must be:
   - A) fast  (B) idempotent  (C) silent  (D) global
5. The lineage key tying an index entry to its source is:
   - A) the embedding  (B) source_ref  (C) the page number  (D) a hash
6. Rebuilding a derived index after an edit is safe because:
   - A) indexes are fast  (B) it is derived from the source of truth  (C) SQLite allows it  (D) of caching
7. In a mixed-version deploy window, what must hold:
   - A) only new code works  (B) both old and new code work  (C) nothing  (D) only reads
8. `alembic check` is useful for detecting:
   - A) slow queries  (B) model/DB schema drift  (C) deadlocks  (D) memory leaks

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
