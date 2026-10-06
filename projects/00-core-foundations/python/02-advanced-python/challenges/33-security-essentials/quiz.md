# Challenge 33 — Quiz: Security Essentials

1. `hash_password("x")` twice produces different digests because:
   - A) PBKDF2 is randomized  (B) each call draws a fresh random salt  (C) of ASLR  (D) of timing
2. `verify_password` must compare with:
   - A) `==`  (B) `hmac.compare_digest` (timing-safe)  (C) `is`  (D) hashing twice
3. The digest is:
   - A) 16 bytes, salt 32  (B) 32 bytes, salt 16  (C) both 64  (D) variable
4. SQL injection is blocked by:
   - A) escaping quotes  (B) `?` placeholders (parameterized queries only)  (C) stored procedures  (D) lowercasing
5. `find("1' OR '1'='1")` returns:
   - A) all rows  (B) `[]` (the string is treated as a literal id)  (C) raises  (D) one row
6. YAML is parsed with `yaml.safe_load` only, so `!!python/object/apply:...`:
   - A) executes  (B) raises `yaml.YAMLError`  (C) is skipped  (D) warns
7. `is_safe_path` must call `.resolve()` before containment checks because:
   - A) paths are relative  (B) `..` segments must be normalized before `is_relative_to`  (C) of symlinks only  (D) of case
8. `is_safe_path(root, "../etc/passwd")`:
   - A) returns the path  (B) raises `ValueError` (outside root)  (C) returns `None`  (D) creates the file

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
