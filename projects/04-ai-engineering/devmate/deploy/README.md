# Deploying DevMate (A4)

Target: **Render** (Docker web services + managed Postgres/Redis) with an external
**Qdrant Cloud** cluster, a cheap **Groq** model for generation, and **OpenAI** for
embeddings (Groq has no embeddings endpoint). Everything is driven by `render.yaml`
(a Render Blueprint) plus a few secrets you set in the dashboard.

> This runbook was written and the container build was verified locally
> (`docker compose build devmate-api` then `/health` returns 200). The cloud
> steps need your Render and Qdrant accounts and are not runnable from here.

## Prerequisites

- This repo pushed to GitHub.
- A [Render](https://render.com) account.
- A [Groq](https://console.groq.com) API key (generation) and an OpenAI API key
  (embeddings only; Groq serves no embeddings).
- A [Qdrant Cloud](https://cloud.qdrant.io) free cluster (1 GB).

## Step 1 — Qdrant Cloud

1. Create a free cluster. Copy its **endpoint host** and **API key**.
2. Note the REST port (`6333`). You will set `QDRANT_HOST`, `QDRANT_PORT`,
   `QDRANT_API_KEY` in Render.

## Step 2 — Deploy the Blueprint

1. Render Dashboard -> **New** -> **Blueprint** -> select this repo.
2. Render reads `render.yaml` and creates: `devmate-db` (Postgres),
   `devmate-redis`, `devmate-api`, `devmate-ui`.
3. When prompted, fill the `sync:false` variables: `GROQ_API_KEY`,
   `OPENAI_API_KEY`, `QDRANT_HOST`, `QDRANT_PORT`, `QDRANT_API_KEY`.
   `SECRET_KEY` is generated.

## Step 3 — First boot

1. Wait for `devmate-api` to go live; Render polls `healthCheckPath: /health`.
2. Open the API URL, then `https://<your-api>.onrender.com/health` should return
   `{"status":"healthy",...}`.
3. Open the UI URL (`https://<your-ui>.onrender.com`) and ask a question.

## Step 4 — Load the demo corpus (REQUIRED, currently open)

The `/ingest` endpoint takes a **server-side path**, and the production image has
no repository on disk, so the demo needs a corpus baked into the image and
ingested on boot. Recommended (not yet built):

- Add a small `sample_corpus/` to the image.
- Add a startup hook that ingests it when the Qdrant collection is empty.

Until that lands, `/ask` and the UI will answer over an empty index. Tracked as
task 6 in `docs/deployment-plan.md`.

## Step 5 — Smoke test

```bash
curl https://<your-api>.onrender.com/health
curl -X POST https://<your-api>.onrender.com/ai/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"what does this project do?","stream":false}'
```

## Roll back

Render keeps the previous successful deploy per service: open the service ->
**Events** -> **Rollback** to the prior deploy.

## Cold starts (free plan)

Free web services sleep after ~15 minutes idle and take ~30-60 s to wake. The
README and the demo page should say so; optionally add an uptime pinger.

## Free-plan caveats

- Render's free Postgres is time-limited (currently 30 days); recreate or move to
  a paid plan before it expires.
- Free Redis and free web services have small memory limits; the API is capped at
  2 GB in compose but Render free is smaller, so watch for OOM on heavy ingests.
