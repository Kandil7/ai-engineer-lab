# Auto Checkpoint (pre-compaction snapshot)

- Time: 2026-10-02T12:44:39.645Z
- Session: ses_f03b47a43ffeC8rdXc1PhPnR1G
- Project: D:\AI\Projects\ai-engineer-lab

## Recent user messages (tail)
- **user**: commit all changes one commit per one file in detials
- **user**: what is left
- **user**: commit all changes one commit per one file in detials
- **user**: commit all changes one commit per one file in detials
- **user**: commit all changes one commit per one file in detials
- **user**: commit all changes one commit per one file in detials
- **user**: commit all changes one commit per one file in detials
- **user**: commit all changes one commit per one file in detials
- **user**: Refresh the architecture visualization for an indexed project.

## Steps

### 1. Detect project

- If `` is provided: use it as the project path or name.
- If no arguments: use the current working directory.
- Resolve the project name (lowercase directory name).

### 2. Verify index exists

Call `codebase-memory-mcp_list_projects` to confirm the project is indexed. If not, suggest running `/cbm-init` first.

### 3. Get fresh architecture data

Call `codebase-memory-mcp_get_architecture` with:
- `project`: the project name
- `aspects`: `["all"]`

Also call:
- `codebase-memory-mcp_search_graph(project="<name>", label="Function", min_degree=5, limit=20)` — hotspots
- `graphify_god_nodes()` — most-connected nodes
- `graphify_graph_stats()` — graph statistics

### 4. Get graphify insights (if available)

If the project has a graphify graph:
- `graphify_query_graph(query="MATCH (n)-[r]->(m) RETURN n, type(r), m LIMIT 50")` — relationships
- `graphify_get_community()` — community structure

### 5. Regenerate Mermaid diagram

From fresh data, synthesize an updated Mermaid `graph TD`:

**Rules:**
- Max 30 nodes. Summarize low-degree nodes into cluster labels.
- Short labels (function name only).
- Subgraphs for packages/clusters.
- Highlight hotspots (red), entry points (blue), god nodes (orange).
- Cross-package edges with labels.

**Layout:**
```mermaid
graph TD
    subgraph "Entry Points"
        main["main()"]
    end
    subgraph "Core"
        core_logic["Core Logic"]
    end
  
- **user**: Initialize codebase-memory-mcp + graphify for the current or specified project.

## Available MCP tools (server prefixes)

- `codebase-memory-mcp_*` — structural graph (index, search, trace, architecture)
- `graphify_*` — multimodal graph (query, god_nodes, shortest_path, PR impact)
- `repomix_*` — context packing (pack_codebase, grep output)
- `code-review-graph_*` — review blast-radius (detect_changes, get_impact_radius)

## Steps

### 1. Detect project

- If `` is provided: use it as the project path or name.
  - If it's a path (contains `/` or `\`), resolve it.
  - If it's a name, look under `D:\AI\Projects\<name>`.
- If no arguments: use the current working directory.
- Verify the path exists and contains source code.

### 2. Check index status

Call `codebase-memory-mcp_list_projects` to see if this project is already indexed.

- If indexed: call `codebase-memory-mcp_index_status` to get current stats.
- If not indexed: proceed to step 3.

### 3. Index the project (if needed)

Call `codebase-memory-mcp_index_repository` with:
- `repo_path`: the detected project root
- `project`: derived project name (lowercase, hyphens for spaces)
- `mode`: `"full"`

Report indexing progress. Wait for completion.

### 4. Get architecture data

Call `codebase-memory-mcp_get_architecture` with:
- `project`: the project name
- `aspects`: `["all"]`

This returns: languages, packages, entry points, routes, hotspots, boundaries, layers, clusters, cycles, file tree.

### 5. Generate Mermaid di

> Regenerate a curated checkpoint with /checkpoint.