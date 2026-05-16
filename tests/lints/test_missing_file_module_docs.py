"""Tests for the ``missing_file_module_docs`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_missing_file_module_docs(tmp_path: Path) -> None:
    """Test run detects missing_file_module_docs violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub fn calculate(x: i32) -> i32 {\n    x * 2\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "missing_file_module_docs" in result.output
    assert "help: add module-level documentation using `//!`" in result.output


def test_run_missing_file_module_docs_clean(tmp_path: Path) -> None:
    """Test run passes when no missing_file_module_docs violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "//! This module provides data processing utilities.\n\npub fn process(data:"
        "&str) -> String {\n    data.to_uppercase()\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[missing_file_module_docs]:" not in result.output
