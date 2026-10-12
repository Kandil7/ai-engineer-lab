"""
MCP (Model Context Protocol) Server for DevMate.

Exposes DevMate's retrieval capabilities to any MCP-compatible client.
"""

from collections.abc import Sequence
from typing import Any

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from devmate.config import settings
from devmate.index.embeddings import embedding_service
from devmate.retrieve.retriever import get_retriever


class DevMateMCPServer:
    """MCP Server exposing DevMate tools."""

    def __init__(self) -> None:
        self.server = Server("devmate")
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Register MCP tools."""

        @self.server.list_tools()
        async def list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="search_code",
                    description="Search for code snippets, functions, or patterns in the repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query - keywords, function names, or natural language",
                            },
                            "language": {
                                "type": "string",
                                "description": "Optional: filter by programming language",
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                ),
                types.Tool(
                    name="read_file",
                    description="Read the full content of a file from the repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Relative path to the file from repository root",
                            },
                        },
                        "required": ["file_path"],
                    },
                ),
                types.Tool(
                    name="get_repo_stats",
                    description="Get repository statistics and overview",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[types.TextContent]:
            if name == "search_code":
                return await self._search_code(arguments)
            if name == "read_file":
                return await self._read_file(arguments)
            if name == "get_repo_stats":
                return await self._get_repo_stats()
            raise ValueError(f"Unknown tool: {name}")

    async def _search_code(self, arguments: dict[str, Any]) -> Sequence[types.TextContent]:
        """Search code in the repository."""
        query = arguments.get("query", "")
        language = arguments.get("language")
        top_k = arguments.get("top_k", 5)

        if not query:
            return [types.TextContent(type="text", text="Error: query is required")]

        try:
            retriever = await get_retriever()

            # Generate query embedding
            embedding_result = await embedding_service.embed([query])
            query_vector = embedding_result.embeddings[0]

            # Build filter
            filter_dict = {}
            if language:
                filter_dict["language"] = language

            # Retrieve
            results = await retriever.retrieve(
                query=query,
                query_vector=query_vector,
                filter=filter_dict,
                use_reranker=True,
            )

            # Format results
            if not results:
                return [types.TextContent(type="text", text="No results found.")]

            formatted = []
            for i, result in enumerate(results[:top_k], 1):
                result.metadata.get("source", "unknown")
                filename = result.metadata.get("filename", "unknown")
                chunk_type = result.metadata.get("chunk_type", "")
                name = result.metadata.get("name", "")

                formatted.append(
                    f"## Result {i}: {filename}"
                    f"{f' | {chunk_type}' if chunk_type else ''}"
                    f"{f' | {name}' if name else ''}"
                    f" (relevance: {result.score:.3f})\n\n```\n{result.content[:1000]}\n```"
                )

            return [types.TextContent(type="text", text="\n\n---\n\n".join(formatted))]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Search error: {str(e)}")]

    async def _read_file(self, arguments: dict[str, Any]) -> Sequence[types.TextContent]:
        """Read a file from the repository."""
        file_path = arguments.get("file_path", "")

        if not file_path:
            return [types.TextContent(type="text", text="Error: file_path is required")]

        try:
            from pathlib import Path

            repo_root = Path.cwd()
            full_path = (repo_root / file_path).resolve()

            # Security check
            try:
                full_path.relative_to(repo_root)
            except ValueError:
                return [types.TextContent(type="text", text="Error: Path traversal not allowed")]

            if not full_path.exists():
                return [types.TextContent(type="text", text=f"Error: File not found: {file_path}")]

            if not full_path.is_file():
                return [types.TextContent(type="text", text=f"Error: Not a file: {file_path}")]

            content = full_path.read_text(encoding="utf-8")

            return [types.TextContent(type="text", text=f"# {file_path}\n\n```\n{content}\n```")]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Read error: {str(e)}")]

    async def _get_repo_stats(self) -> Sequence[types.TextContent]:
        """Get repository statistics."""
        try:
            from devmate.index.vector_store import get_vector_store

            vs = await get_vector_store()
            count = await vs.count()

            stats = f"""# Repository Statistics

- **Total indexed chunks**: {count}
- **Vector store**: Qdrant ({settings.qdrant_collection})
- **Embedding model**: {settings.embedding_model}
- **Embedding dimensions**: {settings.embedding_dimensions}
"""
            return [types.TextContent(type="text", text=stats)]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Stats error: {str(e)}")]

    async def run_stdio(self) -> None:
        """Run the MCP server over stdio."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )

    async def run_http(self, host: str = "0.0.0.0", port: int = 8001) -> None:
        """Run the MCP server over HTTP (SSE)."""
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request) -> None:
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await self.server.run(
                    streams[0],
                    streams[1],
                    self.server.create_initialization_options(),
                )

        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request._send)
            return Response("")

        app = Starlette(
            routes=[
                Route("/sse", handle_sse),
                Mount("/messages/", app=handle_messages),
            ],
        )

        import uvicorn

        config = uvicorn.Config(app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()


# Global MCP server instance
_mcp_server_instance: DevMateMCPServer | None = None


async def get_mcp_server() -> DevMateMCPServer:
    """Get or create global MCP server."""
    global _mcp_server_instance

    if _mcp_server_instance is None:
        _mcp_server_instance = DevMateMCPServer()

    return _mcp_server_instance


async def run_mcp_stdio() -> None:
    """Run MCP server over stdio (for CLI usage)."""
    server = await get_mcp_server()
    await server.run_stdio()


async def run_mcp_http(host: str = None, port: int = None) -> None:
    """Run MCP server over HTTP."""
    server = await get_mcp_server()
    await server.run_http(
        host=host or settings.mcp_host,
        port=port or settings.mcp_port,
    )


def main() -> None:
    """CLI entry: `python -m devmate.mcp.server [stdio|http]` (default stdio).

    stdio is what local MCP clients (opencode, Claude Desktop) expect.
    """
    import asyncio
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if mode == "http":
        asyncio.run(run_mcp_http())
    else:
        asyncio.run(run_mcp_stdio())


if __name__ == "__main__":
    main()
