"""
CLI for DevMate - stats, ask, ingest commands.
"""

import asyncio
import json
import sys
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from datetime import UTC
from pathlib import Path
from typing import cast

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from devmate.index.vector_store import get_vector_store
from devmate.ingest.chunker import DocumentLoader, get_chunker
from devmate.llm.client import StreamingChunk
from devmate.retrieve.rag import get_rag_pipeline


def _force_utf8_console() -> None:
    """Windows cp1252 consoles choke on Rich's braille spinner (\\u2807)."""
    for stream in (sys.stdout, sys.stderr):
        encoding = getattr(stream, "encoding", "") or ""
        if encoding.lower() != "utf-8" and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]


_force_utf8_console()

app = typer.Typer(name="devmate", help="AI Assistant for Code Repositories")
console = Console()


@dataclass
class RepoStats:
    """Collected repository statistics: chunk aggregates plus AST analysis."""

    path: str
    total_chunks: int
    total_characters: int
    total_lines: int
    file_types: dict[str, int] = field(default_factory=dict)
    languages: dict[str, int] = field(default_factory=dict)
    ast_files: int = 0
    ast_total_lines: int = 0
    ast_code_lines: int = 0
    ast_functions: int = 0
    ast_classes: int = 0
    ast_file_types: dict[str, int] = field(default_factory=dict)


def collect_repo_stats(repo_path: Path) -> RepoStats:
    """Load documents, aggregate chunk statistics, run AST analysis."""
    loader = DocumentLoader()
    documents = list(loader.load_repository(repo_path))

    stats = RepoStats(
        path=str(repo_path),
        total_chunks=len(documents),
        total_characters=0,
        total_lines=0,
    )
    for doc in documents:
        ext = doc.metadata.get("extension", "unknown")
        stats.file_types[ext] = stats.file_types.get(ext, 0) + 1
        stats.total_characters += len(doc.content)
        stats.total_lines += doc.content.count("\n") + 1
        lang = doc.metadata.get("language", "unknown")
        stats.languages[lang] = stats.languages.get(lang, 0) + 1

    from devmate.ingest.repo_reader import RepoAnalyzer

    repo_stats = RepoAnalyzer().analyze(repo_path)
    stats.ast_files = repo_stats.total_files
    stats.ast_total_lines = repo_stats.total_lines
    stats.ast_code_lines = repo_stats.total_code_lines
    stats.ast_functions = repo_stats.total_functions
    stats.ast_classes = repo_stats.total_classes
    stats.ast_file_types = dict(repo_stats.file_types)
    return stats


def format_stats_json(stats: RepoStats) -> str:
    """Serialize collected statistics to the JSON document the CLI prints."""
    return json.dumps(
        {
            "path": stats.path,
            "total_chunks": stats.total_chunks,
            "total_characters": stats.total_characters,
            "total_lines": stats.total_lines,
            "file_types": stats.file_types,
            "languages": stats.languages,
            "ast": {
                "files": stats.ast_files,
                "total_lines": stats.ast_total_lines,
                "code_lines": stats.ast_code_lines,
                "functions": stats.ast_functions,
                "classes": stats.ast_classes,
                "file_types": stats.ast_file_types,
            },
        },
        indent=2,
    )


def present_stats_table(stats: RepoStats, repo_name: str) -> None:
    """Print the summary, file-type, language, and AST tables."""
    console.print(f"\n[bold cyan]Repository Statistics: {repo_name}[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Chunks", str(stats.total_chunks))
    table.add_row("Total Characters", f"{stats.total_characters:,}")
    table.add_row("Total Lines", f"{stats.total_lines:,}")
    table.add_row("Unique File Types", str(len(stats.file_types)))
    console.print(table)

    ft_table = Table(show_header=True, header_style="bold magenta")
    ft_table.add_column("Extension", style="cyan")
    ft_table.add_column("Count", style="green")
    for ext, count in sorted(stats.file_types.items(), key=lambda x: -x[1]):
        ft_table.add_row(ext, str(count))
    console.print("\n[bold]File Types:[/bold]")
    console.print(ft_table)

    lang_table = Table(show_header=True, header_style="bold magenta")
    lang_table.add_column("Language", style="cyan")
    lang_table.add_column("Chunks", style="green")
    for lang, count in sorted(stats.languages.items(), key=lambda x: -x[1]):
        lang_table.add_row(lang, str(count))
    console.print("\n[bold]Languages:[/bold]")
    console.print(lang_table)

    py_table = Table(show_header=True, header_style="bold magenta")
    py_table.add_column("Metric", style="cyan")
    py_table.add_column("Value", style="green")
    py_table.add_row("Files", str(stats.ast_files))
    py_table.add_row("Total Lines", f"{stats.ast_total_lines:,}")
    py_table.add_row("Code Lines", f"{stats.ast_code_lines:,}")
    py_table.add_row("Functions", f"{stats.ast_functions:,}")
    py_table.add_row("Classes", f"{stats.ast_classes:,}")
    console.print("\n[bold]Repository Analysis (AST):[/bold]")
    console.print(py_table)


@app.command()
def stats(
    path: str = typer.Argument(".", help="Path to repository"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
) -> None:
    """Analyze repository statistics."""
    repo_path = Path(path).resolve()

    if not repo_path.exists():
        console.print(f"[red]Path not found: {repo_path}[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing repository...", total=None)
        collected = collect_repo_stats(repo_path)
        progress.update(
            task, description=f"Found {collected.total_chunks} chunks, computing stats..."
        )
        progress.update(task, description="Complete!")

    if format == "json":
        console.print_json(format_stats_json(collected))
    else:
        present_stats_table(collected, repo_path.name)


@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask"),
    stream: bool = typer.Option(True, "--stream/--no-stream", help="Stream response"),
    repo: str = typer.Option(".", "--repo", "-r", help="Repository path"),
) -> None:
    """Ask a question about the repository."""
    asyncio.run(_ask_async(question, stream, repo))


async def _ask_async(question: str, stream: bool, repo: str) -> None:
    Path(repo).resolve()

    # Check if repo is indexed
    try:
        vs = await get_vector_store()
        count = await vs.count()
        if count == 0:
            console.print("[yellow]Repository not indexed. Run 'devmate ingest' first.[/yellow]")
            return
    except Exception as e:
        console.print(f"[red]Vector store not available: {e}[/red]")
        return

    rag_pipeline = await get_rag_pipeline()

    from devmate.retrieve.rag import RAGRequest as InternalRAGRequest
    from devmate.retrieve.rag import RAGResult

    request = InternalRAGRequest(query=question, stream=stream)

    if stream:
        console.print(f"\n[bold cyan]Question:[/bold cyan] {question}\n")
        console.print("[bold green]Answer:[/bold green]")

        stream_result = await rag_pipeline.query(request)
        async for chunk in cast(AsyncIterator[StreamingChunk], stream_result):
            console.print(chunk.content, end="", highlight=False)
        console.print()
    else:
        raw_result = await rag_pipeline.query(request)
        result = cast(RAGResult, raw_result)
        console.print(f"\n[bold cyan]Question:[/bold cyan] {question}")
        console.print(f"\n[bold green]Answer:[/bold green] {result.answer}")

        if result.contexts:
            console.print("\n[bold]Sources:[/bold]")
            for i, ctx in enumerate(result.contexts[:3], 1):
                source = ctx.metadata.get("source", "unknown")
                console.print(f"  [{i}] {source} (score: {ctx.score:.3f})")


@app.command()
def ingest(
    path: str = typer.Argument(".", help="Path to repository"),
    chunker: str = typer.Option(
        "fixed", "--chunker", "-c", help="Chunker: fixed, recursive, ast_aware"
    ),
    chunk_size: int = typer.Option(512, "--chunk-size", help="Chunk size in tokens"),
    chunk_overlap: int = typer.Option(50, "--chunk-overlap", help="Chunk overlap in tokens"),
) -> None:
    """Ingest a repository into the vector store."""
    asyncio.run(_ingest_async(path, chunker, chunk_size, chunk_overlap))


async def _ingest_async(path: str, chunker_name: str, chunk_size: int, chunk_overlap: int) -> None:
    repo_path = Path(path).resolve()

    if not repo_path.exists():
        console.print(f"[red]Path not found: {repo_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Ingesting repository: {repo_path.name}[/cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Loading documents...", total=None)

        chunker = get_chunker(chunker_name, chunk_size=chunk_size, overlap=chunk_overlap)
        loader = DocumentLoader(chunker=chunker)
        documents = list(loader.load_repository(repo_path))

        progress.update(
            task, description=f"Loaded {len(documents)} chunks. Generating embeddings..."
        )

        rag_pipeline = await get_rag_pipeline()
        chunks_created = await rag_pipeline.ingest_documents(documents)

        progress.update(task, description="Complete!")

    console.print(
        f"[green]✓[/green] Ingested {len(documents)} documents, created {chunks_created} vectors"
    )


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
) -> None:
    """Start the API server."""
    import uvicorn

    uvicorn.run(
        "devmate.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def cost(
    days: int = typer.Option(7, "--days", "-d", help="Days of history"),
) -> None:
    """Show cost and usage statistics."""
    from datetime import datetime, timedelta

    from devmate.obs.cost import cost_tracker

    since = datetime.now(UTC) - timedelta(days=days)
    summary = cost_tracker.get_summary(since=since)

    console.print(f"\n[bold cyan]Usage Statistics (Last {days} days)[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Requests", str(summary.total_requests))
    table.add_row("Total Tokens", f"{summary.total_tokens:,}")
    table.add_row("Total Cost", f"${summary.total_cost_usd:.6f}")
    table.add_row(
        "Avg Latency", f"{summary.total_latency_ms / max(summary.total_requests, 1):.2f}ms"
    )

    console.print(table)

    if summary.by_model:
        model_table = Table(show_header=True, header_style="bold magenta")
        model_table.add_column("Model", style="cyan")
        model_table.add_column("Requests", style="green")
        model_table.add_column("Tokens", style="yellow")
        model_table.add_column("Cost", style="red")
        model_table.add_column("Avg Latency", style="blue")

        for model, data in sorted(summary.by_model.items(), key=lambda x: -x[1]["cost"]):
            model_table.add_row(
                model,
                str(int(data["requests"])),
                f"{int(data['tokens']):,}",
                f"${data['cost']:.6f}",
                f"{data['latency_ms'] / max(data['requests'], 1):.2f}ms",
            )

        console.print("\n[bold]By Model:[/bold]")
        console.print(model_table)


if __name__ == "__main__":
    app()
