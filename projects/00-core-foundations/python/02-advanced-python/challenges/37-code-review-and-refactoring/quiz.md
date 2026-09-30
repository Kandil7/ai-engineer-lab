# Challenge 37 — Quiz: Code Review and Refactoring

1. Cyclomatic complexity counts:
   - A) lines  (B) independent execution paths  (C) parameters  (D) imports
2. A lock test proves that a refactor:
   - A) is fast  (B) preserves behavior  (C) reduces lines  (D) passes CI
3. The right way to measure "this function is too complex":
   - A) opinion  (B) branch/complexity counts  (C) file size  (D) git blame
4. Extract-method refactors should split by:
   - A) line count  (B) responsibility  (C) alphabet  (D) author
5. Replace-conditional-with-polymorphism moves the branch into:
   - A) the caller  (B) strategy classes + composition root  (C) config  (D) tests
6. A refactoring PR may also change behavior:
   - A) always  (B) never — split the PRs  (C) only on Fridays  (D) if small
7. The four parts of a review comment are:
   - A) name, file, line, emoji  (B) severity, location, problem, fix  (C) bug, fix, test, ship  (D) what, why, how, when
8. `ast` is preferable to regex for measuring code because:
   - A) it is faster  (B) it parses structure correctly  (C) regex is deprecated  (D) it needs no imports

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
