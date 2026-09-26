"""Unit tests for the `devmate stats` CLI command (devmate.cli.main.stats)."""

import json
import re
from pathlib import Path

from typer.testing import CliRunner

from devmate.cli.main import app

runner = CliRunner()


def _write_repo(tmp_path: Path) -> Path:
    """Small fixture repo: one Python file, one Markdown file, one binary."""
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "main.py").write_text(
        'def add(a: int, b: int) -> int:\n    """Add two numbers."""\n    return a + b\n',
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Sample\n\nBody text for chunking.\n", encoding="utf-8")
    (tmp_path / "blob.bin").write_bytes(b"\x00\x01\x02\x03")
    return tmp_path


def test_stats_missing_path_exits_nonzero(tmp_path: Path) -> None:
    result = runner.invoke(app, ["stats", str(tmp_path / "does-not-exist")])
    assert result.exit_code == 1
    assert "Path not found" in result.output


def test_stats_json_format(tmp_path: Path) -> None:
    repo = _write_repo(tmp_path)
    result = runner.invoke(app, ["stats", str(repo), "--format", "json"])
    assert result.exit_code == 0, result.output

    # console.print_json pretty-prints; recover the JSON object from the output
    match = re.search(r"\{.*\}", result.output, re.DOTALL)
    assert match, f"no JSON in output:\n{result.output}"
    payload = json.loads(match.group(0))

    assert payload["path"] == str(repo)
    assert payload["total_chunks"] > 0
    assert payload["total_characters"] > 0
    assert payload["total_lines"] > 0
    # .md and .py chunks are counted; the binary is skipped by the loader
    assert set(payload["file_types"]) == {".md", ".py"}
    # AST analysis saw the Python file, its function, and zero classes
    assert payload["ast"]["files"] >= 1
    assert payload["ast"]["functions"] >= 1
    assert payload["ast"]["classes"] == 0


def test_stats_table_format(tmp_path: Path) -> None:
    repo = _write_repo(tmp_path)
    result = runner.invoke(app, ["stats", str(repo)])
    assert result.exit_code == 0, result.output

    assert "Repository Statistics" in result.output
    assert "Total Chunks" in result.output
    assert "File Types" in result.output
    assert ".py" in result.output
    assert ".md" in result.output
    # AST section is present in table mode too
    assert "Repository Analysis (AST)" in result.output
    assert "Functions" in result.output


def test_stats_deterministic_across_runs(tmp_path: Path) -> None:
    """Same repo -> identical chunk/character counts (deterministic hashing)."""
    repo = _write_repo(tmp_path)
    runs = []
    for _ in range(2):
        result = runner.invoke(app, ["stats", str(repo), "--format", "json"])
        assert result.exit_code == 0, result.output
        match = re.search(r"\{.*\}", result.output, re.DOTALL)
        payload = json.loads(match.group(0))
        runs.append((payload["total_chunks"], payload["total_characters"], payload["total_lines"]))
    assert runs[0] == runs[1]
