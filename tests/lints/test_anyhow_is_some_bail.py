"""Tests for the ``anyhow_is_some_bail`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_is_some_bail(tmp_path: Path) -> None:
    """Test run detects anyhow_is_some_bail violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if entries.next().is_some() {\n    bail!("Path is not empty");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_is_some_bail" in result.output
    assert (
        "help: use ensure! with is_none() instead of if/is_some/bail!" in result.output
    )


def test_run_anyhow_is_some_bail_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_is_some_bail violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'if entries.next().is_some() {\n    println!("Found entry");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_is_some_bail]:" not in result.output
