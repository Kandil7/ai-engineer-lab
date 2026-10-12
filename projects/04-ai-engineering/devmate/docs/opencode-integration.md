# Using DevMate inside opencode (MCP integration)

DevMate ships an MCP server (`devmate.mcp.server`) that exposes three tools to
any MCP client: `search_code`, `read_file`, and `get_repo_stats`. Registering it
in opencode lets the agent ask DevMate (RAG over the indexed repo) while you work.

## 1. Prereqs

The MCP server reads the same settings as the app, so it needs:

- A reachable Qdrant collection with the repo indexed (see `deploy/README.md`).
- The embeddings provider configured (Ollama locally, or Jina/OpenAI in the
  cloud) — same `EMBEDDING_*` vars as the API.
- The `.env` in `projects/04-ai-engineering/devmate/` (or the vars passed via
  `environment` below).

If the vector store is empty, `search_code` returns "No results found."; index
the repo first with `python -m devmate.cli ingest <path>` or `POST /ingest`.

## 2. Register the server in opencode

Add to your opencode config (`~/.config/opencode/opencode.jsonc`) under `mcp`:

```jsonc
"mcp": {
  "devmate": {
    "type": "local",
    "command": [
      "D:\\AI\\Projects\\ai-engineer-lab\\projects\\04-ai-engineering\\devmate\\.venv\\Scripts\\python.exe",
      "-m", "devmate.mcp.server"
    ],
    "enabled": true,
    "environment": {
      "DEFAULT_LLM_PROVIDER": "groq",
      "GROQ_API_KEY": "<groq key>",
      "EMBEDDING_PROVIDER": "openai",
      "EMBEDDING_BASE_URL": "https://api.jina.ai/v1",
      "EMBEDDING_MODEL": "jina-embeddings-v3",
      "EMBEDDING_DIMENSIONS": "1024",
      "EMBEDDING_API_KEY": "<jina key>",
      "QDRANT_VECTOR_SIZE": "1024",
      "QDRANT_HOST": "<qdrant host>",
      "QDRANT_PORT": "6333",
      "QDRANT_HTTPS": "true",
      "QDRANT_API_KEY": "<qdrant key>"
    }
  }
}
```

Restart opencode, then the `devmate` MCP tools appear in the agent's toolset.

## 3. Notes

- **stdio, not http.** Local MCP clients spawn the process and talk over stdio;
  `python -m devmate.mcp.server` defaults to stdio (`http` is opt-in for a
  remote client).
- **Secrets.** `~/.config/opencode/opencode.jsonc` is outside the repo, but it
  now holds keys; keep it out of any Git repo and rotate if it leaks.
- **Recursion is the point.** Point DevMate at this repo and opencode can ask
  it "how does the eval gate work?" and get grounded, cited chunks.

## 4. Roadmap (not built)

- `devmate learn` MCP tool: expose the Learning OS knowledge registry so opencode
  can answer "what should I learn to build X" (ties DevMate to the registry).
- A DevMate **skill** in opencode that documents the tools and when to use them.
