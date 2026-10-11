# Deploying DevMate on Railway

Railway deploys from a GitHub repo and is **usage-based** (no free tier; you get
a small trial credit, then pay for usage). Two services come from the same image:
the API and the Streamlit UI. Postgres and Redis are Railway database services.

> The container builds and runs locally (`docker compose build devmate-api`;
> `/health` returns 200), and the Dockerfile already binds to `$PORT`, which
> Railway injects. The cloud steps below need your Railway account.

## Prerequisites

- This repo pushed to GitHub (`Kandil7/ai-engineer-lab`).
- A [Railway](https://railway.com) account with GitHub connected.
- A Groq API key (generation), a free OpenAI-compatible embeddings key (Jina),
  and a reachable Qdrant cluster.

## Step 1 — Create the project and configure the API service

1. Railway -> **New Project** -> **Deploy from GitHub repo** -> select the repo.
2. Open the service -> **Settings** -> **Source**:
   - **Branch:** set to **`master`** (this repo's default; Railway defaults to
     `main`, which does not exist here).
   - **Root Directory:** `projects/04-ai-engineering/devmate`.
3. **Build** -> set **Builder** to **Dockerfile** (not Railpack) and
   **Dockerfile Path** = `docker/Dockerfile` (relative to the Root Directory).
   Railpack would try to build it as a plain Python app and miss the start command.
4. **Deploy** -> **Healthcheck Path** = `/health`. Leave the Start Command empty:
   the Dockerfile's CMD already runs `uvicorn ... --port ${PORT}`.

> Railway is deprecating Config-as-Code (`railway.toml`); configure via this
> Settings screen. The `railway.toml` in the repo is kept for reference only.

## Step 2 — Add Postgres and Redis

1. **New** -> **Database** -> **PostgreSQL**.
2. **New** -> **Database** -> **Redis**.

Railway exposes each as variables you can reference from the API service.

## Step 3 — Set the API variables

In the API service -> **Variables**, add:

```
APP_ENV=production
DEBUG=false
DEFAULT_LLM_PROVIDER=groq
DEFAULT_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=<groq key>

EMBEDDING_PROVIDER=openai
EMBEDDING_BASE_URL=https://api.jina.ai/v1
EMBEDDING_MODEL=jina-embeddings-v3
EMBEDDING_DIMENSIONS=1024
EMBEDDING_API_KEY=<jina key>
QDRANT_VECTOR_SIZE=1024

QDRANT_HOST=<cluster host>
QDRANT_PORT=6333
QDRANT_HTTPS=true
QDRANT_API_KEY=<qdrant key>

DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=<any long random string>

RATE_LIMIT_REQUESTS=20
RATE_LIMIT_WINDOW_SECONDS=60
```

`DATABASE_URL` from Railway is `postgresql://...`; the app normalizes it to
`postgresql+asyncpg://` automatically.

## Step 4 — Public URL

Service -> **Settings** -> **Networking** -> **Generate Domain**. Railway routes
to the container's `$PORT`; `GET /health` should return `{"status":"healthy"}`.

## Step 5 — Add the UI service (optional)

1. **New** -> **GitHub Repo** -> same repo, same Root Directory.
2. Set a **Custom Start Command**:
   `streamlit run ui/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
3. Add `DEVMATE_API_URL` = the API service's public URL (from Step 4).
4. Generate a domain for the UI.

## Rollback

Deployments -> pick a previous successful deploy -> **Redeploy**.

## Notes

- **Qdrant must be reachable.** Until the cluster returns 200 (not 403), the API
  still starts and `/health` is green, but the demo answers over an empty index.
- **Cost:** Railway bills usage (CPU/RAM/egress). A free demo that sleeps a lot
  is cheap but not zero; watch the usage panel.
- **Secrets:** set them only in Railway; never commit them.
