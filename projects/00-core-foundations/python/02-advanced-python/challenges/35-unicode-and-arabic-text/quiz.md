# Challenge 35 — Quiz: Unicode and Arabic Text

1. `unicodedata.normalize("NFKC", "\ufefb")` produces:
   - A) the same char  (B) `لا` (two code points)  (C) `ل`  (D) `""`
2. Stripping harakat from `مُحَمَّد` gives:
   - A) `محمد`  (B) `محم`  (C) `مُحمد`  (D) unchanged
3. For search keys, ta marbuta (ة) is folded to:
   - A) `ت`  (B) `ه`  (C) `ط`  (D) nothing
4. `int("٣")` raises:
   - A) TypeError  (B) ValueError  (C) nothing, returns 3  (D) OverflowError
5. In UTF-8, the Arabic letter ل (U+0644) occupies:
   - A) 1 byte  (B) 2 bytes  (C) 3 bytes  (D) 4 bytes
6. The best grouping structure for deduplicating 5000 records by search_key:
   - A) pairwise loop  (B) dict.setdefault  (C) sorted list  (D) nested for-loops
7. A streaming importer keeps memory bounded by holding only:
   - A) the whole file  (B) one batch  (C) all errors  (D) nothing
8. Reading a file without `encoding=` on Windows risks:
   - A) nothing  (B) locale-encoding mojibake  (C) faster reads  (D) a warning

**Answers:** 1-B, 2-A, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
