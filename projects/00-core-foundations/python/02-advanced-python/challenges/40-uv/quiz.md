# Challenge 40: uv — Quiz

8 questions on the mechanics a learner plausibly gets wrong.

**Answers:** 1-B, 2-C, 3-B, 4-B, 5-B, 6-C, 7-B, 8-B

1. A wheel is named `pkg-1.0-cp39-abi3-win_amd64.whl`. On CPython 3.12 /
   Windows it is:
   - A) Rejected, because cp39 != cp312
   - B) Accepted, because abi3 wheels built for an older CPython run on any later 3.x
   - C) Accepted only on Linux
   - D) Rejected because the abi tag is not cp312

2. In `name-version-pythontag-abitag-platformtag.whl`, why is a plain split
   on `-` safe?
   - A) Wheels never contain more than 5 parts
   - B) The parser strips build tags first
   - C) Distribution names are normalized so `-` becomes `_`
   - D) It is not; you need a regex

3. `WheelIndex` parses each filename once at construction instead of per
   query because:
   - A) Filenames change between queries
   - B) 200 wheels x 100 queries is 20,000 re-parses vs 200
   - C) The parse callable is expensive to import
   - D) select() would otherwise return unsorted results

4. For `audit_stream`, comparing `2.10.0` against `fixed_in 2.9.9` as
   strings would wrongly report:
   - A) 2.10.0 as vulnerable
   - B) 2.10.0 as vulnerable, because "2.10" < "2.9" lexicographically
   - C) nothing; string comparison is correct here
   - D) 2.9.9 as vulnerable

5. A version exactly equal to `fixed_in` is:
   - A) Vulnerable
   - B) Not vulnerable; the fix landed in that version
   - C) Vulnerable only if the advisory has no id
   - D) Undefined behavior

6. The Gold guard asserts peak memory under 1 MB for 20,000 packages. The
   naive shape that fails is:
   - A) Sorting the findings list
   - B) `packages = list(packages)` before processing
   - C) Using a dict for advisories
   - D) Lowercasing package names

7. `audit_exit_code` returning 1 on findings is the CI contract because:
   - A) uv requires exit code 1 for any output
   - B) Pipelines gate on the exit code without parsing output
   - C) JSON output cannot carry severity
   - D) Exit code 0 means the lock is stale

8. `fixed_in: None` in an advisory means:
   - A) The package is safe
   - B) No fix is available; the finding must be ignored or the package removed
   - C) The advisory is malformed and skipped
   - D) The version comparison is skipped
