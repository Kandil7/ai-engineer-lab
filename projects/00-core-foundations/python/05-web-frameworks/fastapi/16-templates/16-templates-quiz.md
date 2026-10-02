# FastAPI 16: Templates — Quiz

> **Topic Overview**: Jinja2 rendering and autoescaping.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you render an HTML template in FastAPI?**
- A) `Jinja2Templates(...).TemplateResponse(...)`
- B) `render(...)`
- C) `app.html(...)`
- D) `template(...)`

<details><summary>Reveal Answer</summary>**A.** Jinja2 templates.</details>

### Question 2 — Easy
**What does autoescaping do?**
- A) Minifies
- B) Escapes HTML in variables to prevent XSS
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** XSS defense.</details>

### Question 3 — Medium
**When is autoescaping typically on/off?**
- A) Always off
- B) On for `.html` templates; off for other extensions by default
- C) Always on
- D) Random

<details><summary>Reveal Answer</summary>**B.** Extension-based default.</details>

### Question 4 — Medium
**What is the risk of `|safe`?**
- A) None
- B) It disables escaping, so untrusted content can inject script
- C) Slower
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Turn off only for trusted HTML.</details>

### Question 5 — Medium
**When do you choose templates over a JSON API?**
- A) Always
- B) Server-rendered pages (admin, docs), not JSON clients
- C) Never
- D) For mobile only

<details><summary>Reveal Answer</summary>**B.** HTML consumers.</details>

### Question 6 — Hard
**How do you pass context to a template?**
- A) The `context` dict argument
- B) Query string
- C) A header
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Context mapping.</details>

### Question 7 — Hard
**Why keep business logic out of templates?**
- A) Speed
- B) Templates are presentation; logic belongs in the handler for testability
- C) Caching
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Separation of concerns.</details>

### Question 8 — Hard
**What is a common XSS mistake with templates?**
- A) Using autoescape
- B) Rendering user input with `|safe` or `Markup`
- C) Passing context
- D) Using Jinja

<details><summary>Reveal Answer</summary>**B.** Never trust user HTML.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You render templates safely. |
| 5-6 | Review escaping and context. |
| < 5 | Re-read the lecture. |
