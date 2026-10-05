# 🐍 Python Learning Module — AI Engineer Lab

> **3,069 files across 9 learning phases** — from `print("Hello")` to production ML pipelines and GenAI systems.
> Each topic ships with a self-contained directory containing exercise, lecture, and glossary.

---

## 📋 Quick Navigation

| Phase | Directory | Focus |
|-------|-----------|-------|
| **1** | `01-core-python/` | Python fundamentals: basics → control-flow → functions → OOP → advanced |
| **2** | `02-advanced-python/` | Decorators → async → metaclasses → design patterns → Unicode → maintainable code → test strategy |
| **3** | `03-libraries/` | NumPy, Pandas, Matplotlib, SciPy, Polars |
| **4** | `04-databases/` | SQL, PostgreSQL, MongoDB, Redis, SQLAlchemy, Vector Stores, migrations, backups |
| **5** | `05-web-frameworks/` | FastAPI (runnable), Django (reference-only) |
| **6** | `06-data-structures-algorithms/` | Arrays → trees → sorts → searches |
| **7** | `07-machine-learning/` | Fundamentals → Advanced → Deep Learning |
| **8** | `08-mlops/` | Reproducibility → registry → serving → monitoring → A/B |
| **9** | `09-genai/` | LLMs → RAG → agents → eval → fine-tuning → production |
| **10** | `10-system-design/` | **[NEW]** Component contracts → queues → consistency → failure modes → ADRs |
| 📚 | `supplementary/` | Quizzes + interview prep |
| 🏆 | `projects/` | Capstone mini-projects combining all phases |
| 🗺️ | `SKILLS_MASTERY_MAP.md` | **[NEW]** Six professional skills → topics → Athar mastery evidence |

---

## 🚀 Getting Started

```bash
# 1. Requirements
pip install -r requirements.txt

# 2. Start with Phase 1
cd 01-core-python/basics/01-introduction
python 01-introduction.py

# 3. Follow the learning path
# See: learning_path.md for the recommended order

# 4. Verify everything works
python run_smoke_tests.py
```

---

## 🏗️ Directory Structure

```
python/
├── 01-core-python/                  # 📘 Phase 1: Python Fundamentals
│   ├── basics/                      # 16 topics: Introduction to Collections
│   │   ├── 01-introduction/
│   │   │   ├── 01-introduction.py
│   │   │   ├── 01-introduction-lecture.md
│   │   │   └── 01-introduction-glossary.md
│   │   └── ... (16 topics)
│   ├── control-flow/                # 4 topics: Conditionals and Loops
│   ├── functions/                   # 14 topics: Functions, Modules, Error Handling
│   ├── oop/                         # 5 topics: Object-Oriented Programming
│   ├── advanced/                    # 13 topics: Advanced Topics
│   ├── practice/                    # Practice problems
│   └── README.md
│
├── 02-advanced-python/              # 🔬 Phase 2: Advanced Python
│   ├── 01-decorators/
│   │   ├── 01-decorators.py
│   │   ├── 01-decorators-lecture.md
│   │   └── 01-decorators-glossary.md
│   ├── ... (34 original topics)
│   ├── 35-unicode-and-arabic-text/  # [NEW] Unicode, normalization, Arabic text
│   ├── 36-separation-of-concerns/   # [NEW] Layers, Protocols, DI, config, logging
│   ├── 37-code-review-and-refactoring/ # [NEW] Review lenses, smells, lock tests
│   ├── 38-test-strategy-contract-regression/ # [NEW] Unit/integration/contract/regression/data
│   └── 39-poetry/                   # [NEW] Poetry: constraints, lockfile audit, groups
│
├── 03-libraries/                    # 📊 Phase 3: Data Science Libraries
│   ├── numpy/                       # 34 topics: Arrays, ufuncs, linear algebra
│   │   ├── 01-introduction/
│   │   └── ... (34 topics)
│   ├── pandas/                      # DataFrames, cleaning, analysis
│   │   ├── basics/                  # 24 topics: W3Schools series
│   │   ├── advanced/                # 21 topics: Professional series
│   │   ├── production/              # 6 topics: Method chaining, memory, pitfalls
│   │   └── case-studies/            # 2 topics: Real-world examples
│   ├── matplotlib/                  # Visualization
│   │   ├── basics/                  # 12 topics: W3Schools series
│   │   ├── advanced/                # 16 topics: OO API, styling, ML viz
│   │   └── 3d/                      # 5 topics: 3D plotting
│   ├── scipy/                       # 16 topics: Scientific computing
│   └── polars/                      # 6 topics: Modern DataFrame library
│
├── 04-databases/                    # 🗄️ Phase 4: Database Integration
│   ├── sql-fundamentals/            # 14 topics: Core SQL concepts
│   ├── sql-sqlite/                  # 12 topics: SQLite exercises
│   ├── postgresql/                  # 7 topics: PostgreSQL exercises + [NEW] backup/restore
│   ├── mongodb/                     # 12 topics: MongoDB exercises
│   ├── redis/                       # 8 topics: Caching, pub/sub, sessions
│   ├── sqlalchemy/                  # 11 topics: ORM patterns + [NEW] migrations
│   └── vector-stores/               # 8 topics: Embeddings, similarity search
│
├── 05-web-frameworks/               # 🌐 Phase 5: Backend Development
│   ├── fastapi/                     # 52 topics: Routing, auth, websockets
│   └── django/                      # 20 topics: Reference guides
│
├── 06-data-structures-algorithms/   # ⚙️ Phase 6: DSA
│   ├── 01-introduction/
│   │   ├── 01-introduction.py
│   │   ├── 01-introduction-lecture.md
│   │   └── 01-introduction-glossary.md
│   └── ... (20 topics)
│
├── 07-machine-learning/             # 🤖 Phase 7: Machine Learning
│   ├── fundamentals/                # 23 topics: Basic ML concepts
│   ├── advanced/                    # 12 topics: Pipelines, metrics, tuning
│   └── deep-learning/               # 5 topics: PyTorch, neural nets, transformers
│
├── 08-mlops/                        # 🚀 Phase 8: MLOps (Production ML)
├── 09-genai/                        # 🧠 Phase 9: GenAI (LLMs, RAG, Agents)
├── 10-system-design/                # 🏗️ Phase 10: System Design [NEW]
│   ├── 01-component-contracts/      # Contracts, compatibility, migration paths
│   ├── 02-queues-and-workflows/     # Jobs, at-least-once, idempotency, DLQ
│   ├── 03-consistency-and-staleness/# Truth vs derived, drift, caches, rebuild
│   ├── 04-failure-modes-and-resilience/ # FMEA, timeouts, bulkheads, degradation
│   └── 05-architecture-decision-records/ # ADR format, lifecycle, enforcement
├── supplementary/                   # 📚 Quizzes (80) + Interview prep (18)
├── projects/                        # 🏆 Capstone Mini-Projects
├── tests/                           # ✅ Unit tests (328 passing)
└── learning_path.md                 # 🗺️ Full learning map
```

---

## 📖 Learning Path

See **[learning_path.md](learning_path.md)** for the complete, week-by-week learning schedule covering all 10 phases.

**Recommended order:** Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 4 → Phase 6 → Phase 7 → Phase 8 → Phase 9 → Phase 10 → Projects

---

## ✅ Quick Start by Goal

| If you want to... | Start here |
|-------------------|------------|
| Learn Python from scratch | `01-core-python/basics/01-introduction/01-introduction.py` |
| Master advanced Python | `02-advanced-python/01-decorators/01-decorators.py` |
| Do data science | `03-libraries/numpy/01-introduction/01-introduction.py` |
| Build web APIs | `05-web-frameworks/fastapi/01-introduction/01-introduction.py` |
| Learn SQL/NoSQL | `04-databases/sql-fundamentals/01-relational-model/01-relational-model.py` |
| Practice algorithms | `06-data-structures-algorithms/01-introduction/01-introduction.py` |
| Build ML models | `07-machine-learning/fundamentals/01-getting-started/01-getting-started.py` |
| Ship ML to production | `08-mlops/01-reproducibility.py` |
| Build LLM/RAG/agents | `09-genai/01-llm-fundamentals.py` |
| Learn system design (contracts, queues, consistency, ADRs) | `10-system-design/01-component-contracts/` |
| Master the Athar skills track | `SKILLS_MASTERY_MAP.md` |
| Practice production Python (Arabic text, batching) | `02-advanced-python/challenges/35-unicode-and-arabic-text/` |
| Practice maintainable code (swappable engines) | `02-advanced-python/challenges/36-separation-of-concerns/` |
| Practice testing (provenance, idempotency) | `02-advanced-python/challenges/38-test-strategy-contract-regression/` |
| Practice dependency management (constraints, lockfiles) | `02-advanced-python/challenges/39-poetry/` |
| Practice database ops (migrations, backups) | `04-databases/sqlalchemy/challenges/11-migrations-alembic/` |
| Prep for interviews | `supplementary/interviews/` |
| Test yourself | `supplementary/quizzes/` |
| Build a project | `projects/01-calculator/` |

---

## 📝 Notes

- Each `.py` file is **self-contained** and runnable with `python filename.py`
- All FastAPI files can be served with `uvicorn filename:app --reload`
- Matplotlib plots save to `./output/` (no display required; headless with `MPLBACKEND=Agg`)
- MySQL exercises use built-in `sqlite3` — no driver needed
- MongoDB exercises use Python dicts as document stand-ins
- Django is **reference-only**: not installed by default and excluded from smoke tests
- Quiz files are `.md` — edit them or use as flashcards
- Interview files contain both questions AND solutions
- Run the suite: `python -m pytest tests -q`
- **Challenge sets** (Bronze/Silver/Gold) live in each module's `challenges/`
  directory. Default runs target `starter.py` and fail with
  `NotImplementedError` until solved; validate a reference with
  `$env:CHALLENGE_USE_SOLUTION = "1"` before `python -m pytest`

---

## 📦 Dependencies

See [requirements.txt](requirements.txt) for the full list.
Most Phase 1–2 exercises need **no external packages**.

---

## 🔗 Related Resources

- [AI Engineer Lab (root)](../../../README.md)
- [Project Plans](../../../docs/plan/)
- [Architecture Docs](../../../docs/architecture/)
- [Infrastructure](../../../infra/)

---

*Last updated: September 2026*
