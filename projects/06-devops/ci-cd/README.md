# CI/CD — Continuous Integration & Deployment

GitHub Actions workflows for automated testing, building, and deployment of all services
in the Full-Stack AI Engineer Lab.

---

## Workflow Overview

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Push /  │ ──→ │   Test   │ ──→ │  Build   │ ──→ │  Deploy  │
│   PR     │     │  Suite   │     │  Images  │     │  to Env  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

---

## GitHub Actions Workflows

### 1. CI Workflow (`ci.yml`)

**Trigger:** Push to `main`, pull requests

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-go:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: cd projects/01-backend-go/01-auth-service && go test ./...
      - run: cd projects/01-backend-go/01-auth-service && go vet ./...

  test-flutter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          channel: 'stable'
      - run: cd projects/02-frontend/flutter-app && flutter test

  validate-repo:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run registry validators
        shell: pwsh
        run: |
          foreach ($suite in @("prompts", "workflows", "templates", "registries", "repo-structure")) {
            & "tests/$suite/validate.ps1"
            if ($LASTEXITCODE -ne 0) { exit 1 }
          }
```

### 2. Build Workflow (`build.yml`)

**Trigger:** Tags matching `v*`, manual dispatch

```yaml
name: Build & Push
on:
  push:
    tags: ['v*']
  workflow_dispatch:

jobs:
  docker-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}/auth-service:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 3. Deploy Workflow (`deploy.yml`)

**Trigger:** Successful build workflow completion

```yaml
name: Deploy
on:
  workflow_run:
    workflows: ["Build & Push"]
    types: [completed]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          # Deploy to staging environment
          echo "Deploying to staging..."
```

---

## Test Automation

### Test Matrix

| Service          | Test Type      | Framework   | Command                          |
| ---------------- | -------------- | ----------- | -------------------------------- |
| auth-service     | Unit           | Go test     | `go test ./...`                  |
| auth-service     | Integration    | Go test     | `go test -tags=integration ./...`|
| flutter-app      | Unit + Widget  | flutter_test| `flutter test`                   |
| flutter-app      | Integration    | integration_test| `flutter test integration_test/`|
| nextjs-web       | Unit           | Vitest      | `npm run test`                   |
| nextjs-web       | E2E            | Playwright  | `npx playwright test`            |
| prompts          | Validation     | PowerShell  | `./tests/prompts/validate.ps1`   |
| workflows        | Validation     | PowerShell  | `./tests/workflows/validate.ps1` |
| templates        | Validation     | PowerShell  | `./tests/templates/validate.ps1` |
| registries       | Validation     | PowerShell  | `./tests/registries/validate.ps1`|

### Coverage Requirements

| Service          | Minimum Coverage |
| ---------------- | ---------------- |
| Go backend       | 80%              |
| Flutter          | 70%              |
| Next.js          | 70%              |

---

## Build Pipeline

### Docker Image Build

```yaml
# Build arguments for optimization
ARG BUILDPLATFORM=linux/amd64
ARG TARGETPLATFORM=linux/amd64

# Multi-platform builds
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t ghcr.io/org/repo:latest .
```

### Image Tagging Strategy

| Tag Pattern         | Purpose                  |
| ------------------- | ------------------------ |
| `latest`            | Most recent main build   |
| `v1.2.3`            | Semantic version release |
| `sha-abc1234`       | Specific commit build    |
| `staging`           | Staging environment      |

---

## Environment Management

### Environments

| Environment  | Branch    | Auto-deploy | Purpose              |
| ------------ | --------- | ----------- | -------------------- |
| Development  | feature/* | No          | Local development    |
| Staging      | main      | Yes         | Pre-production test  |
| Production   | tags      | Manual gate | Live deployment      |

### Secrets Management

| Secret               | Purpose                  |
| -------------------- | ------------------------ |
| `POSTGRES_PASSWORD`  | Database password        |
| `OPENAI_API_KEY`     | OpenAI API access        |
| `JWT_SECRET`         | JWT signing key          |
| `REDIS_URL`          | Redis connection string  |

Store in GitHub Settings → Secrets → Actions.

---

## Quality Gates

Every PR must pass before merge:

1. **All tests pass** — unit, integration, validation
2. **Coverage threshold** — no decrease from main
3. **Linting passes** — no new warnings or errors
4. **Security scan** — no critical vulnerabilities
5. **Build succeeds** — Docker images build without errors

---

## Getting Started

```bash
# Trigger CI locally (simulate GitHub Actions)
act -j test-go

# View workflow runs
gh run list

# View specific run logs
gh run view <run-id> --log

# Manually trigger a workflow
gh workflow run build.yml -f version=1.0.0
```
