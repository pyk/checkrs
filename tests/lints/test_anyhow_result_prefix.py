"""Tests for the ``anyhow_result_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_result_prefix(tmp_path: Path) -> None:
    """Test run detects anyhow_result_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn create_database(&self) -> anyhow::Result<Database> {\n"
        "    // ...\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_result_prefix" in result.output
    assert (
        "help: import anyhow::Result and use it without the anyhow:: prefix"
        in result.output
    )


def test_run_anyhow_result_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_result_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use anyhow::Result;\n\n"
        "pub fn create_database(&self) -> Result<Database> {\n"
        "    // ...\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_result_prefix]:" not in result.output
