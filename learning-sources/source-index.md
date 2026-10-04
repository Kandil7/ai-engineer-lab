# Learning Source Index

Resources specifically selected for the `fullstack-ai-engineer-lab` stack:
FastAPI + PostgreSQL/Redis/Qdrant + LLMs/RAG + Agents.

**Rule:** Few sources, many projects. Every source → artifact in the repo.

---

## Legend

| Status | Meaning |
|--------|---------|
| `planned` | Identified but not started |
| `in-progress` | Currently studying |
| `completed` | Finished; source note exists in `docs/learning/source-summaries/` |

---

## Level 1: Web / Full-Stack Foundations

### Courses & Platforms

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 1 | FreeCodeCamp – Full Stack Curriculum | course | HTML, CSS, JS, React, APIs, backend | planned | [freecodecamp.org](https://www.freecodecamp.org/) | HTML/CSS/JS → `projects/00-core-foundations/`. REST APIs → FastAPI. |
| 2 | The Odin Project – Full Stack JavaScript | course | Full-Stack JS, project-based | planned | [theodinproject.com](https://www.theodinproject.com/) | Project folders, tests, git workflow mirror the lab philosophy. Apply every Odin project inside the lab. |
| 3 | Scrimba – Fullstack Developer Path | course | JS, React, Next, Node, SQL, TypeScript | planned | [scrimba.com](https://scrimba.com/) | Interactive sections for React/Next → optional. Node concepts → mental model for FastAPI. |
| 4 | App Academy Open | course | Bootcamp-style full-stack | planned | [appacademy.io](https://www.appacademy.io/) | Free alternative to Scrimba. Use for backend + database sections. |

### How to Use

- **FreeCodeCamp + Odin** for basics (months 1-3):
  - HTML/CSS/JS → `projects/00-core-foundations/`
  - REST APIs → FastAPI
  - Write `docs/learning/paths/web-basics.md` for each module
- **Scrimba/App Academy** for structured backend + database sections:
  - Connect every course project to a lab project

---

## Level 2: Backend / DevOps / Git

### Backend & Git

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 5 | Fullstack + AI Web Dev Roadmap (YouTube) | video | Why start with Python/FastAPI then move to AI | planned | [YouTube](https://www.youtube.com/watch?v=uB6orI_RpmY) | Understand why the lab uses FastAPI after web fundamentals. |
| 6 | Git/GitHub for AI Engineers | video | Git workflow for AI projects | planned | [YouTube](https://www.youtube.com/watch?v=enBm0jLXLZ4) | Write `docs/decisions/000x-git-branching-strategy.md`. Apply feature branches per service. |
| 7 | Pro Git (free book) | book | Git internals, branching, merging | planned | [git-scm.com](https://git-scm.com/book/en/v2) | Deep reference for Git decisions in the lab. |

### DevOps & Docker

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 8 | Docker/Deployment course (from Mimo list) | course | Docker, CI/CD, deployment | planned | [mimo.org](https://mimo.org/blog/best-web-development-courses) | Pick ONE course. Apply to `projects/06-devops/docker/` and `infra/docker-compose.yml`. |
| 9 | Docker Compose Specification | doc | Services, volumes, networks | planned | [docs.docker.com](https://docs.docker.com/compose/) | Reference when modifying `infra/docker/docker-compose.yml`. |
| 10 | PostgreSQL 16 Documentation | doc | SQL, indexing, JSONB | planned | [postgresql.org](https://www.postgresql.org/docs/16/) | Every service → apply one schema/query example → document in `docs/learning/deep-dives/`. |
| 11 | Redis Commands Reference | doc | Data types, transactions, pub/sub | planned | [redis.io](https://redis.io/commands/) | Same approach — one command per session in `projects/03-databases/redis-cache/`. |

### How to Use

- **Git/GitHub video** → write branching strategy ADR
- **Docker course** → containerize the API service, deploy to Render/Vercel/VPS
- **PostgreSQL/Redis docs** → apply one concept per service build session

---

## Level 3: AI Engineering / LLMs / RAG / Agents

### ML & LLMs Fundamentals

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 12 | ML for Beginners (Microsoft) | course | ML fundamentals, practical exercises | planned | [GitHub](https://github.com/microsoft/ML-For-Beginners) | Write `docs/learning/paths/ai-foundations.md`. Apply concepts to `projects/04-ai-engineering/`. |
| 13 | Neural Networks: Zero to Hero (Karpathy) | course | Neural nets from scratch | planned | [YouTube](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) | Build intuition for how LLMs work. Write deep-dive in `docs/learning/deep-dives/transformers.md`. |
| 14 | Machine Learning Specialization (Andrew Ng) | course | Supervised learning, basics | planned | [Coursera](https://www.coursera.org/specializations/machine-learning-introduction) | ONE course only. Understand concepts, don't train models from scratch. |
| 15 | MIT Intro to Deep Learning | course | Deep learning foundations | planned | [MIT](https://introtodeeplearning.com/) | Supplementary to Andrew Ng. Focus on intuition, not math proofs. |

### Transformers & NLP

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 16 | Hugging Face NLP/LLM Course | course | Transformers → practical usage | planned | [huggingface.co](https://huggingface.co/learn/nlp-course) | Apply to `projects/04-ai-engineering/embeddings/` and `rag-system/`. |
| 17 | Illustrated Transformer (Jay Alammar) | article | Attention mechanism, visual explanation | planned | [jalammar.github.io](https://jalammar.github.io/illustrated-transformer/) | Write `docs/learning/deep-dives/transformers.md`. Foundation for understanding RAG retrieval. |

### RAG / Fine-tuning / Agents

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 18 | Cohere LLM University | course | Practical LLM usage | planned | [cohere.com](https://docs.cohere.com/docs/llmu) | Apply LLM patterns to `.ai/prompts/` and `projects/04-ai-engineering/`. |
| 19 | DeepLearning.AI – Pretraining LLMs | course | Pretraining concepts | planned | [deeplearning.ai](https://www.deeplearning.ai/) | Reference for Baligh/Baleeg-style projects (outside this repo). |
| 20 | DeepLearning.AI – Fine-tuning LLMs | course | Fine-tuning patterns | planned | [deeplearning.ai](https://www.deeplearning.ai/) | Reference for Baligh/Baleeg-style projects. |
| 21 | DeepLearning.AI – RAG | course | RAG pipeline: chunk → embed → retrieve → generate | planned | [deeplearning.ai](https://www.deeplearning.ai/) | Design `projects/04-ai-engineering/rag-system/`. Document in `docs/learning/deep-dives/rag-system-deep-dive.md`. |
| 22 | DeepLearning.AI – Multi-agent Systems (CrewAI) | course | Multi-agent orchestration | planned | [deepleasoning.ai](https://www.deeplearning.ai/) | Strengthen `.ai/prompts/roles/` and `.ai/workflows/`. |
| 23 | Hugging Face Agents Course | course | Agent fundamentals, tool use | planned | [huggingface.co](https://huggingface.co/learn/agents-course) | Apply to `projects/04-ai-engineering/agents/`. |
| 24 | Berkeley LLM Agents Course | course | Advanced agent research | planned | [YouTube](https://www.youtube.com/watch?v=U07MHi4Suj8) | Deep reference for `.ai/prompts/`, `.ai/workflows/`, `docs/architecture/ai-workspace-architecture.md`. |
| 25 | Arize AI – AI Agents Mastery | course | Monitoring, eval, guardrails | planned | [arize.com](https://arize.com/) | Apply to `evaluations/`, `docs/decisions/`, governance patterns. |

### How to Use

- **ML for Beginners + Karpathy** → write AI foundations path
- **HF NLP Course + Illustrated Transformer** → build embeddings project
- **DeepLearning.AI RAG** → design rag-system project
- **HF Agents + Berkeley + Arize** → strengthen agent prompts and evaluation

---

## Reference: AI Engineering Lab Repos

| # | Source | Type | Topic | Status | Link | Lab Integration |
|---|--------|------|-------|--------|------|-----------------|
| 26 | AI Engineering Lab – Government (UK) | repo | Guidance, templates, training materials for AI labs | planned | [GitHub](https://github.com/govuk-digital-backbone/aiengineeringlab) | Compare structure, templates, guidance with this lab. Borrow patterns for `docs/`, `templates/`. |
| 27 | GitHub AI Engineering Repos List | list | ML for Beginners, Hands-On LLMs, Prompt Engineering Guide, etc. | planned | [Instagram](https://www.instagram.com/p/DYY3mdkDKo8/) | Use as meta-index in this source file. Pick 1-2 per skill level. |

---

## Lab Integration Map

Every source maps to specific lab paths:

```
Source → Read/Watch
    ↓
Extract: Key concepts + one example + one exercise
    ↓
Apply in lab project:
    - projects/00-core-foundations/     (basics)
    - projects/03-databases/            (PostgreSQL/Redis/Qdrant)
    - projects/04-ai-engineering/       (AI/LLMs/RAG/Agents)
    - projects/05-system-design/        (architecture)
    - projects/06-devops/               (Docker/deployment)
    - projects/07-capstone/             (ThanaweyaGPT)
    ↓
Document in:
    - docs/learning/paths/<topic>.md
    - docs/learning/source-summaries/<source>.md
    - docs/learning/deep-dives/<topic>.md
    ↓
Review using .ai/prompts/roles/code-reviewer.md
    ↓
Reflect in docs/learning/notes/weekly/
```

---

## Resource Priority

### Tier 1: Start Here (Months 1-3)
1. **FreeCodeCamp** — HTML/CSS/JS basics
2. **The Odin Project** — project-based foundations
3. **YouTube Crash Course** — quick language intro

### Tier 2: Build Backend Foundations (Months 4-6)
4. **FastAPI docs** — API service patterns
5. **Roadmap.sh** — visual coverage reference

### Tier 3: Master Databases + DevOps (Months 7-9)
6. **PostgreSQL/Redis docs** — apply one concept per session
7. **Docker course** — containerize and deploy

### Tier 4: AI Engineering (Months 10-12)
8. **ML for Beginners + Karpathy** — ML foundations
9. **HF NLP Course + Illustrated Transformer** — Transformers
10. **DeepLearning.AI RAG + Agents courses** — RAG + Agents
11. **Arize AI** — evaluation and monitoring

### Don't Collect
- Pick ONE per tier, COMPLETE it, then move on
- Every source → artifact in the repo
- Use docs + hands-on guides for supplementary topics

---

## How to Use This Index

1. **Add a source**: Append a row with status `planned`. Assign unique `#`.
2. **Start studying**: Change status to `in-progress`. Create source note using template.
3. **Complete**: Change status to `completed`. Ensure source note exists in `docs/learning/source-summaries/`.
4. **Link to project**: Each source note must link to at least one lab project.

```powershell
# Generate a source note from template
./infra/scripts/new-source-note.ps1 "huggingface-nlp-course" doc
```
