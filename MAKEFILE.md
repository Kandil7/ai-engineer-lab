# Makefile Reference

This repo targets **Windows/PowerShell**, so automation lives in `infra/scripts/*.ps1` rather
than a Makefile. This document is the comprehensive reference for every command and operation
available in the workspace.

> **Prerequisites:** PowerShell 5.1+, Go 1.22+, Docker Desktop (optional).
> The `tests/*` validators are standalone PowerShell scripts (not Pester tests);
> run them directly or via `make validate`.

---

## Table of Contents

- [Infrastructure Commands](#infrastructure-commands)
- [Development Commands](#development-commands)
- [Validation Commands](#validation-commands)
- [Project Commands](#project-commands)
- [Daily Workflow Commands](#daily-workflow-commands)
- [Learning Workflow Commands](#learning-workflow-commands)
- [Evaluation Commands](#evaluation-commands)

---

## Infrastructure Commands

### Start Local Infrastructure

```powershell
docker compose -f infra/docker/docker-compose.yml up -d
```

Brings up PostgreSQL (5432), Redis (6379), and Qdrant (6333) in the background. All data
persists in Docker volumes between restarts. Use this at the start of every work session.

**When to use:** First thing each day, or after a `docker compose down`.

---

### Start Infrastructure with Dev Tools

```powershell
docker compose -f infra/docker/docker-compose.yml --profile dev-tools up -d
```

Same as above but also starts PgAdmin (5050), Redis Commander (8081), and the Qdrant
dashboard. Useful for visual database inspection.

**When to use:** Debugging data issues, inspecting vector collections, or verifying schema.

---

### Stop Infrastructure

```powershell
docker compose -f infra/docker/docker-compose.yml down
```

Stops all containers but preserves data volumes. Safe to run repeatedly.

---

### Stop and Remove All Data

```powershell
docker compose -f infra/docker/docker-compose.yml down -v
```

Stops containers AND deletes all volumes. This is a full reset — all data is lost.

**When to use:** Starting fresh, fixing corrupted state, or after a failed migration.

---

### Restart a Specific Service

```powershell
docker compose -f infra/docker/docker-compose.yml restart postgres
docker compose -f infra/docker/docker-compose.yml restart redis
docker compose -f infra/docker/docker-compose.yml restart qdrant
```

Restarts a single container without affecting others. Data is preserved.

---

### View Container Logs

```powershell
docker compose -f infra/docker/docker-compose.yml logs -f postgres
docker compose -f infra/docker/docker-compose.yml logs -f redis
docker compose -f infra/docker/docker-compose.yml logs -f qdrant
```

Follows logs in real-time. Press `Ctrl+C` to stop. Omit `-f` for non-following output.

---

### Check Container Health

```powershell
docker compose -f infra/docker/docker-compose.yml ps
```

Shows running status and health check state for all services. All three core services should
show `healthy` before proceeding with development.

---

### Database Migrations

```powershell
# Apply migrations (when migration files exist in projects/03-databases/postgres-design/)
psql -h localhost -p 5432 -U fslab -d fslab -f projects/03-databases/postgres-design/migrations/001_init.sql

# Or via Docker
docker exec -i fslab-postgres psql -U fslab -d fslab < projects/03-databases/postgres-design/migrations/001_init.sql
```

Run SQL migration files against the local PostgreSQL instance. Always back up data before
running destructive migrations.

**When to use:** After schema changes, new table creation, or index updates.

---

### Redis Cache Management

```powershell
# Flush all Redis data
docker exec fslab-redis redis-cli FLUSHALL

# Flush only the current database
docker exec fslab-redis redis-cli FLUSHDB

# Check Redis memory usage
docker exec fslab-redis redis-cli INFO memory
```

**When to use:** After changing cache key patterns, fixing stale data, or debugging cache
misses.

---

### Qdrant Vector DB Setup

```powershell
# List all collections
curl http://localhost:6333/collections

# Check collection info
curl http://localhost:6333/collections/educational_content

# Delete a collection (destructive)
curl -X DELETE http://localhost:6333/collections/educational_content
```

**When to use:** After re-embedding content, changing vector dimensions, or debugging
retrieval quality.

---

## Development Commands

### Run Auth Service Locally

```powershell
cd projects/01-backend-go/01-auth-service
go run .
```

Starts the Go auth service on its default port. Requires PostgreSQL to be running.

**When to use:** Developing or testing authentication features.

---

### Run Auth Service with Hot Reload

```powershell
./infra/scripts/dev-run.ps1
```

Starts the auth service with file watching for automatic restarts on code changes.

**When to use:** Active development where you want instant feedback.

---

### Run Go Tests

```powershell
cd projects/01-backend-go/01-auth-service
go test ./...

# With verbose output
go test -v ./...

# With race detector
go test -race ./...

# Run a specific test
go test -run TestRegisterUser -v ./...
```

**When to use:** Before committing, during development, or after fixing a bug.

---

### Generate New ADR (Architecture Decision Record)

```powershell
./infra/scripts/new-adr.ps1 "Adopt keyset pagination for chat history"
```

Creates a new ADR file from the template in `docs/decisions/`. The next available number is
assigned automatically.

**When to use:** Making any architectural decision that affects system design.

---

### Generate New Code Review

```powershell
./infra/scripts/new-review.ps1 projects/01-backend-go/01-auth-service "JWT refresh token rotation"
```

Creates a code review artifact for a specific project and feature.

**When to use:** After completing a feature implementation, before marking it done.

---

### Generate New Source Note

```powershell
# From official documentation
./infra/scripts/new-source-note.ps1 docs "PostgreSQL JSONB indexing guide"

# From a repository
./infra/scripts/new-source-note.ps1 repo "langchain RAG implementation"

# From a book
./infra/scripts/new-source-note.ps1 book "Designing Data-Intensive Applications chapter 6"

# From a notebook/experiment
./infra/scripts/new-source-note.ps1 notebook "Building a RAG pipeline from scratch"
```

Creates a learning artifact from a study source. The type parameter determines the template.

**When to use:** When studying any external source and want to capture structured learnings.

---

### Seed Database

```powershell
./infra/scripts/seed-db.ps1
```

Populates the database with test data for development. Includes sample users, courses, and
chat sessions.

**When to use:** After a fresh database setup or when you need test data for development.

---

### Initial Project Setup

```powershell
./infra/scripts/setup.ps1
```

One-time setup: validates prerequisites, creates `.env` files, installs Go dependencies,
and optionally runs Docker Compose.

**When to use:** First time cloning the repo, or after a major environment change.

---

## Validation Commands

Each suite is a standalone `tests/<area>/validate.ps1` script. Every suite
exits non-zero on any failure **or warning**, so they gate CI directly (see
the `workspace` job in `.github/workflows/ci.yml`).

### Validate Repository Structure

```powershell
./tests/repo-structure/validate.ps1
```

Validates that the repository follows the expected folder structure: required directories
exist, files are in the right places, and naming conventions are followed.

**When to use:** After refactoring folder structure, or to verify the workspace is intact.

---

### Validate Templates

```powershell
./tests/templates/validate.ps1
```

Checks that all templates in `templates/` are well-formed, have required sections, and
follow the naming convention.

**When to use:** After modifying or adding templates.

---

### Validate Prompts

```powershell
./tests/prompts/validate.ps1
```

Validates prompt files under `.ai/prompts/` for correct structure, required fields, and
consistency with the registry.

**When to use:** After editing or creating new prompts.

---

### Validate Workflows

```powershell
./tests/workflows/validate.ps1
```

Checks workflow files under `.ai/workflows/` for valid step sequences, required artifacts,
and correct cross-references.

**When to use:** After modifying or adding workflows.

---

### Validate Registry Consistency

```powershell
./tests/registries/validate.ps1
```

Checks that the registries agree with each other and with the files on disk: prompt
and workflow frontmatter match their registries, every `prompts_used` /
`used_by` / `used_by_workflows` / `reusable_by` / `pairs_with_roles`
reference resolves, no active prompt is orphaned, and every concrete path
referenced inside `.ai/` exists.

**When to use:** After editing any prompt, workflow, or registry file.

---

### Run All Validations

```powershell
make validate
```

Runs every validation suite in a single pass. This is the pre-commit quality gate.

**When to use:** Before committing changes, at end of work session, or during CI.

---

### Validate a Specific Go Service

```powershell
cd projects/01-backend-go/01-auth-service
go vet ./...
```

Runs Go's static analysis to catch common mistakes: unused imports, unreachable code,
incorrect format strings.

**When to use:** During development, before committing Go code.

---

## Project Commands

### Scaffold a New Service

```powershell
# Create a new Go microservice
$serviceName = "payment-service"
New-Item -ItemType Directory -Path "projects/01-backend-go/$serviceName" -Force
Copy-Item templates/feature-spec.template.md "projects/01-backend-go/$serviceName/feature-spec.md"
```

Creates a new service directory with the standard template structure. Follow the pattern
established by `01-auth-service`.

**When to use:** Starting a new backend service.

---

### Create New Learning Path

```powershell
# Manually create the learning path document
New-Item -ItemType Directory -Path "docs/learning/paths" -Force
# Then create a new .md file following the existing path format
```

Learning paths live in `docs/learning/paths/` and document the sequence of topics for
a specific technology area.

**When to use:** When planning to learn a new technology area systematically.

---

### Add Evaluation Dataset

```powershell
# Create evaluation files in the appropriate subdirectory
# evaluations/rag/ for RAG quality tests
# evaluations/prompts/ for prompt regression tests
# evaluations/projects/ for project-level evaluations
```

Evaluation datasets follow the templates in `templates/evaluation-report.template.md` and
should include input, expected output, and scoring criteria.

**When to use:** When building quality benchmarks for AI features.

---

### Generate Feature Spec

```powershell
# Manually from template
Copy-Item templates/feature-spec.template.md projects/01-backend-go/01-auth-service/feature-spec.md
```

Or use the workflow: start at `.ai/workflows/feature/01-plan.md` which guides you through
creating a complete feature specification.

**When to use:** Before building any new feature.

---

### Generate Architecture Review

```powershell
Copy-Item templates/architecture-review.template.md projects/01-backend-go/01-auth-service/architecture-review.md
```

**When to use:** When a feature touches system boundaries, involves new infrastructure,
or makes cross-service decisions.

---

## Daily Workflow Commands

### Start Daily Loop

```powershell
# Copy today's daily log template
$date = Get-Date -Format "yyyy-MM-dd"
Copy-Item templates/daily-log.template.md "docs/daily-logs/$date.md"
```

The daily loop follows the 6-hour pattern:

| Block  | Time | Activity                                  |
| ------ | ---- | ----------------------------------------- |
| Learn  | 1h   | One topic, docs-first, AI as teacher      |
| Build  | 3h   | One feature in one continuous project     |
| Review | 1h   | AI code review + debugging session        |
| Recall | 1h   | Active recall + notes + plan tomorrow     |

**When to use:** Every work day, at the start of the session.

---

### Generate Daily Log

```powershell
# At end of day, fill in the daily log created at session start
# The template is in templates/daily-log.template.md
```

Document what was learned, built, reviewed, and any open questions for tomorrow.

**When to use:** End of every work session.

---

### Create Weekly Review

```powershell
$date = Get-Date -Format "yyyy-Www"
Copy-Item templates/weekly-review.template.md "docs/reviews/$date-weekly.md"
```

Summarizes the week's progress across all projects, highlights key learnings, and identifies
patterns or blockers.

**When to use:** End of each work week (Friday).

---

### Create Monthly Review

```powershell
$date = Get-Date -Format "yyyy-MM"
Copy-Item templates/monthly-review.template.md "docs/reviews/$date-monthly.md"
```

High-level review of monthly progress, skill development, and project status.

**When to use:** End of each month.

---

## Learning Workflow Commands

### Learn from Documentation

```powershell
# Follow the workflow at:
# .ai/workflows/learning/learn-from-docs.md
```

Structured process for studying official documentation and extracting actionable knowledge.

---

### Learn from a Repository

```powershell
# Follow the workflow at:
# .ai/workflows/learning/learn-from-repo.md
```

Analyze an open-source repository to understand architecture patterns, code conventions,
and implementation decisions.

---

### Learn from a Book

```powershell
# Follow the workflow at:
# .ai/workflows/learning/learn-from-book.md
```

Structured reading with note-taking, concept extraction, and exercise creation.

---

### Learn from a Notebook/Experiment

```powershell
# Follow the workflow at:
# .ai/workflows/learning/learn-from-notebook.md
```

Document experiments, prototypes, and hands-on explorations.

---

## Evaluation Commands

### Run RAG Quality Check

```powershell
# Follow the workflow at:
# .ai/workflows/evaluation/rag-quality-check.md
```

Evaluates RAG retrieval quality: precision, recall, relevance scoring, and failure analysis.

---

### Run Prompt Regression Test

```powershell
# Follow the workflow at:
# .ai/workflows/evaluation/prompt-regression.md
```

Ensures prompt changes don't break existing outputs. Compares before/after results.

---

### Run AI Feature Evaluation

```powershell
# Follow the workflow at:
# .ai/workflows/evaluation/ai-feature-eval.md
```

End-to-end evaluation of AI features against quality criteria and golden test cases.

---

## Quick Reference Card

| Category     | Command                                              | Purpose                    |
| ------------ | ---------------------------------------------------- | -------------------------- |
| **Infra**    | `docker compose up -d`                               | Start databases            |
| **Infra**    | `docker compose down -v`                             | Full reset                 |
| **Dev**      | `go test ./...`                                      | Run Go tests               |
| **Dev**      | `./infra/scripts/new-adr.ps1 "title"`               | New architecture decision  |
| **Dev**      | `./infra/scripts/seed-db.ps1`                        | Populate test data         |
| **Validate** | `make validate`                                    | Run all validations        |
| **Validate** | `./tests/repo-structure/validate.ps1`              | Check folder structure     |
| **Workflow** | `./infra/scripts/new-source-note.ps1 <type> "title"`| Study source               |
| **Workflow** | `./infra/scripts/new-review.ps1 <path> "feature"`   | Code review                |
| **Daily**    | Copy `templates/daily-log.template.md`               | Start daily session        |

---

## Troubleshooting

### Port Already in Use

```powershell
# Find process using port 5432
netstat -ano | findstr :5432
# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Docker Compose Fails to Start

```powershell
# Check Docker Desktop is running
docker info

# Check for orphaned containers
docker compose -f infra/docker/docker-compose.yml ps -a

# Remove orphaned containers
docker compose -f infra/docker/docker-compose.yml rm -f
```

### Go Module Issues

```powershell
cd projects/01-backend-go/01-auth-service
go mod tidy
go mod download
```

### Validator Script Fails to Run

The `tests/*` validators are plain PowerShell scripts. If execution is
blocked, unblock the file or bypass the policy for one run:

```powershell
Unblock-File ./tests/prompts/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File ./tests/prompts/validate.ps1
```
