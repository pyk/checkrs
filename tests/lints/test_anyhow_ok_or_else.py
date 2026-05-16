"""Tests for the ``anyhow_ok_or_else`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_ok_or_else(tmp_path: Path) -> None:
    """Test run detects anyhow_ok_or_else violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'let href = element\n    .value()\n    .attr("href")\n    .ok_or_else(||'
        'anyhow::anyhow!("href attribute not found in item link"))?;\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ok_or_else" in result.output
    assert "help: avoid ok_or_else with anyhow macros" in result.output


def test_run_anyhow_ok_or_else_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_ok_or_else violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let result = option.ok_or_else(|| MyError::NotFound)?;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_ok_or_else]:" not in result.output
