"""Tests for the ``anyhow_map_err`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_map_err(tmp_path: Path) -> None:
    """Test run detects anyhow_map_err violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'let selector = Selector::parse("ul.all-items li a")\n    .map_err(|e|'
        'anyhow::anyhow!("failed to parse HTML selector for item mappings: {}", e))?;\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_map_err" in result.output
    assert "help: avoid map_err with anyhow macros" in result.output


def test_run_anyhow_map_err_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_map_err violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "let result = some_function()\n    .map_err(|e| Box::new(e))?;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_map_err]:" not in result.output
