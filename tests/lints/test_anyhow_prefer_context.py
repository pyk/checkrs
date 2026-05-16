"""Tests for the ``anyhow_prefer_context`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_prefer_context(tmp_path: Path) -> None:
    """Test run detects anyhow_prefer_context violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let dest_path = path_mappings\n    .output_map\n   "
        ".get(&dep.absolute_path)\n    .ok_or_else(|| anyhow::anyhow!(\n       "
        '"Missing output path for dependency {} in path_mappings",\n       '
        "dep.absolute_path.display()\n    ))?;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_prefer_context" in result.output
    assert "help: use context() instead of ok_or_else with anyhow!" in result.output


def test_run_anyhow_prefer_context_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_prefer_context violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "let dest_path = path_mappings\n    .output_map\n   "
        '.get(&dep.absolute_path)\n    .context("Missing output path for dependency in'
        'path_mappings")?;\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_prefer_context]:" not in result.output
