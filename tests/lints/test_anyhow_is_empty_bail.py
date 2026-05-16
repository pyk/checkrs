"""Tests for the ``anyhow_is_empty_bail`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_is_empty_bail(tmp_path: Path) -> None:
    """Test run detects anyhow_is_empty_bail violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if name.trim().is_empty() {\n    bail!("Name cannot be empty");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_is_empty_bail" in result.output
    assert "help: use ensure! with is_empty() instead of if/bail!" in result.output


def test_run_anyhow_is_empty_bail_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_is_empty_bail violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'if name.trim().is_empty() {\n    println!("Name is empty");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_is_empty_bail]:" not in result.output
