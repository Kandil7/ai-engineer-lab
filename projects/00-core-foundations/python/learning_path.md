# 🗺️ Python Learning Path

> **AI Engineer Lab** — Complete learning map through all 9 phases.

---

## 📊 Overview

```
Foundations ──> Libraries ──> Backend ──> Databases ──> DSA ──> ML ──> MLOps ──> GenAI ──> Projects
   Phase 1       Phase 3      Phase 5     Phase 4      Phase 6   Phase 7   Phase 8   Phase 9    🏆
   Phase 2
```

---

## 🚀 Phase 1: Core Python Fundamentals

**Directory:** `01-core-python/`  
**Structure:** `basics/` → `control-flow/` → `functions/` → `oop/` → `advanced/`

| Subdirectory | Topics | Topics |
|--------------|--------|--------|
| **basics/** | 16 | Introduction, Setup, Syntax, Variables, Data Types, Collections |
| **control-flow/** | 4 | If/Else, Match, While Loops, For Loops |
| **functions/** | 14 | Functions, Modules, Error Handling, File I/O |
| **oop/** | 5 | Classes, Inheritance, Polymorphism, Encapsulation |
| **advanced/** | 13 | Pathlib, Dataclasses, Logging, Testing, CLI, Performance |
| **practice/** | 2 | 99 practice problems with solutions |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

**Quick Start:**
```bash
python 01-core-python/basics/01-introduction/01-introduction.py
```

---

## ⚡ Phase 2: Advanced Python

**Directory:** `02-advanced-python/`  
**Topics:** 38 self-contained topic directories

| Order | Topics | Key Concepts |
|-------|--------|--------------|
| 01–05 | Decorators, Generators, Context Managers, Async/Await, Type Hints | Core advanced patterns |
| 06–10 | Dataclasses, Enums, ABCs, Functools, Itertools | Standard library mastery |
| 11–15 | Collections, Properties, Slots, Metaclasses, Descriptors | Object system deep dive |
| 16–20 | Threading, Multiprocessing, Unit Testing, Logging, Design Patterns | Production patterns |
| 21–34 | Concurrency, Asyncio, Typing, Memory, Profiling, Packaging, Security | Expert topics |
| **35** | **Unicode and Arabic text [NEW]** | Normalization, harakat, presentation forms, batch importer |
| **36** | **Separation of concerns [NEW]** | Layers, Protocols, DI, config, logging, engine-swap proof |
| **37** | **Code review and refactoring [NEW]** | Review lenses, smell measurement, lock tests |
| **38** | **Test strategy [NEW]** | Unit/integration/contract/regression/data tests |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

---

## 📊 Phase 3: Data Science Libraries

**Directory:** `03-libraries/`

### NumPy (`numpy/`) — 34 Topics
| Topics | Description |
|--------|-------------|
| 01–03 | Introduction, Getting Started, Creating Arrays |
| 04–07 | Array Indexing, Slicing, Data Types, Copy vs View |
| 08–10 | Array Shape, Reshape, Iterating |
| 11–15 | Array Join, Split, Search, Sort, Filter |
| 16–18 | Random Intro, Data Distribution, Permutation |
| 19–28 | Universal Functions (ufuncs) |
| 29–34 | Broadcasting, Vectorization, Memory, Dtypes, Linear Algebra, Advanced Indexing |

### Pandas (`pandas/`) — 53 Topics
| Subdirectory | Topics | Description |
|--------------|--------|-------------|
| **basics/** | 24 | W3Schools series (beginner-friendly) |
| **advanced/** | 21 | Professional series |
| **production/** | 6 | Method chaining, memory optimization, pitfalls |
| **case-studies/** | 2 | Time series, ML data preparation |

### Matplotlib (`matplotlib/`) — 33 Topics
| Subdirectory | Topics | Description |
|--------------|--------|-------------|
| **basics/** | 12 | W3Schools series |
| **advanced/** | 16 | OO API, styling, ML visualization, saving |
| **3d/** | 5 | Wireframe, surface, 3D scatter/line |

### SciPy (`scipy/`) — 16 Topics
| Topics | Description |
|--------|-------------|
| 01–03 | Introduction, Getting Started, Basic Functions |
| 04–09 | Statistics, Integration, Interpolation, Optimization, Linear Algebra, FFT |
| 10–12 | Spatial Data, Image Processing, I/O |
| 13–16 | Statistical Tests, Optimization Advanced, Sparse Matrices, Distance Metrics |

### Polars (`polars/`) — 6 Topics
| Topics | Description |
|--------|-------------|
| 01–06 | Introduction, Expressions, Lazy Evaluation, Pandas Comparison, PyArrow & Parquet, Larger than Memory |

---

## 🗄️ Phase 4: Databases

**Directory:** `04-databases/`

| Module | Topics | Description |
|--------|--------|-------------|
| **sql-fundamentals/** | 14 | Core SQL (DDL, DML, joins, optimization) |
| **sql-sqlite/** | 12 | SQLite exercises (no installation needed) |
| **postgresql/** | 7 | PostgreSQL with psycopg2 + [NEW] backup/restore |
| **mongodb/** | 12 | MongoDB concepts (dict stand-in) |
| **redis/** | 8 | Caching, pub/sub, distributed locks |
| **sqlalchemy/** | 11 | ORM patterns, async, testing + [NEW] migrations/Alembic |
| **vector-stores/** | 8 | Embeddings, similarity search |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

**Recommended Order:**
```
sql-fundamentals → sql-sqlite → postgresql → mongodb → redis → sqlalchemy → vector-stores
```

---

## 🌐 Phase 5: Web Frameworks

**Directory:** `05-web-frameworks/`

| Framework | Topics | Type |
|-----------|--------|------|
| **fastapi/** | 52 | Runnable (routing, auth, websockets, database) |
| **django/** | 20 | Reference-only (not installed by default) |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

---

## ⚙️ Phase 6: Data Structures & Algorithms

**Directory:** `06-data-structures-algorithms/`  
**Topics:** 20 self-contained topic directories

| Category | Topics |
|----------|--------|
| **Data Structures** | Arrays, Stacks, Queues, Linked Lists, Hash Tables, Trees, Binary Trees, BST, AVL Trees, Graphs |
| **Algorithms** | Linear Search, Binary Search, Bubble Sort, Selection Sort, Insertion Sort, Quick Sort, Counting Sort, Radix Sort, Merge Sort |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

---

## 🤖 Phase 7: Machine Learning

**Directory:** `07-machine-learning/`

| Subdirectory | Topics | Description |
|--------------|--------|-------------|
| **fundamentals/** | 23 | Regression, classification, clustering, PCA |
| **advanced/** | 12 | Pipelines, metrics, tuning, ensembling |
| **deep-learning/** | 5 | PyTorch, neural networks, transformers |

**Each topic directory contains:**
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

**Recommended Order:**
```
fundamentals → advanced → deep-learning
```

---

## 🚀 Phase 8: MLOps (Production Machine Learning)

**Directory:** `08-mlops/`  
**Files:** 16 exercise files (self-verifying)

| # | Topic | Production Concern |
|---|-------|--------------------|
| 1–4 | Reproducibility, Experiment Tracking, Data Versioning, Model Registry | Foundation |
| 5–8 | Packaging, Docker, Serving, Inference Optimization | Deployment |
| 9–12 | Pipelines, Data Validation, Monitoring, CI/CD | Operations |
| 13–16 | Feature Stores, A/B Testing, Cost Optimization, E2E Case Study | Advanced |

---

## 🧠 Phase 9: GenAI (LLMs, RAG, Agents)

**Directory:** `09-genai/`  
**Files:** 25 exercise files (self-verifying)

| # | Topics |
|---|--------|
| 1–5 | LLM fundamentals, API clients, structured output, prompt engineering |
| 6–12 | Embeddings, chunking, RAG baseline, retrieval quality, reranking |
| 13–16 | Tool calling, agent patterns, multi-agent, memory |
| 17–22 | Observability, caching, guardrails, evaluation, fine-tuning |
| 23–25 | Case studies: RAG service, agent, extraction pipeline |

---

## 🏗️ Phase 10: System Design [NEW]

**Directory:** `10-system-design/`  
**Topics:** 5 self-contained topic directories

| # | Topic | Core question |
|---|-------|---------------|
| 01 | Component contracts | What do producer and consumer promise each other? |
| 02 | Queues and workflows | How does slow work survive crashes without duplicating? |
| 03 | Consistency and staleness | What is truth, what is derived, and how do they converge? |
| 04 | Failure modes and resilience | What happens when each component breaks? |
| 05 | Architecture decision records | How do decisions survive the people who made them? |

**Mastery criterion:** explain what happens if a worker fails or the index
becomes older than the source — as a designed story with detections and runbooks.

See `SKILLS_MASTERY_MAP.md` for how this phase maps to the six professional
skills and their Athar mastery evidence.

---

## 🎯 Challenge Sets (practice for every production topic)

Each production topic ships a challenge set with Bronze (~15 min, mechanics) →
Silver (~35 min, right structure) → Gold (~75 min, production constraint).
Silver/Gold tiers include **measured guards** — comparison budgets, call
counts, `tracemalloc` ceilings — never wall-clock assertions.

| Set | Location | Mastery target |
|---|---|---|
| Unicode & Arabic Text | `02-advanced-python/challenges/35-unicode-and-arabic-text/` | streaming import, located errors |
| Separation of Concerns | `02-advanced-python/challenges/36-separation-of-concerns/` | engine-swap invariant |
| Code Review & Refactoring | `02-advanced-python/challenges/37-code-review-and-refactoring/` | lock tests, structural budgets |
| Test Strategy | `02-advanced-python/challenges/38-test-strategy-contract-regression/` | provenance, idempotency, regression gate |
| Migrations | `04-databases/sqlalchemy/challenges/11-migrations-alembic/` | expand-backfill-contract, lineage |
| Backup & Restore | `04-databases/postgresql/challenges/07-backup-and-restore/` | verify-by-restore, PITR |
| Component Contracts | `10-system-design/challenges/01-component-contracts/` | rolling-upgrade plans |
| Queues & Workflows | `10-system-design/challenges/02-queues-and-workflows/` | retry policy, worker accounting |
| Consistency & Staleness | `10-system-design/challenges/03-consistency-and-staleness/` | versioned apply |
| Failure Modes & Resilience | `10-system-design/challenges/04-failure-modes-and-resilience/` | bulkheads, degradation ladder |
| ADRs | `10-system-design/challenges/05-architecture-decision-records/` | decision lifecycle |

```powershell
# default run fails with NotImplementedError until solved
python -m pytest <path>/test_challenge.py -q
# validate the reference solution
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest <path>/test_challenge.py -q
```

---

## 🏆 Capstone Projects

**Directory:** `capstones/`

| Project | Phase Prereqs | Skills Practiced |
|---------|---------------|------------------|
| `01-calculator/` | Phase 1 | Functions, control flow |
| `02-file-manager/` | Phase 1–2 | File I/O, classes, CLI |
| `03-api-server/` | Phase 1–5 | FastAPI, databases, auth |
| `04-data-analyzer/` | Phase 1–3 | Pandas, Matplotlib, NumPy |
| `05-ml-pipeline/` | Phase 1–7 | Scikit-learn, model eval |

---

## 📚 Supplementary Materials

| Resource | Location | Count |
|----------|----------|-------|
| **Quizzes** | `supplementary/quizzes/` | 80 files |
| **Interviews** | `supplementary/interviews/` | 18 files |

---

## 💡 Quick Start

```bash
# 1. Install Python 3.8+
python --version

# 2. (Optional) Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start with Phase 1
cd 01-core-python/basics/01-introduction
python 01-introduction.py

# 5. Run smoke tests
cd ../..
python run_smoke_tests.py
```

---

*Last updated: September 2026*
