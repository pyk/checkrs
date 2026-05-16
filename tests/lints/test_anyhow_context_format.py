"""Tests for the ``anyhow_context_format`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_context_format(tmp_path: Path) -> None:
    """Test run detects anyhow_context_format violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('result.context(format!("error: {}", e))?;\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_context_format" in result.output
    assert (
        "help: use with_context(|| format!()) instead of context(format!())"
        in result.output
    )


def test_run_anyhow_context_format_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_context_format violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('result.context("simple error message")?;\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_context_format]:" not in result.output
