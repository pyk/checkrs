"""Tests for the ``owned_string_parameters`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_owned_string_parameters(tmp_path: Path) -> None:
    """Test run detects owned_string_parameters violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'pub fn show(item_path: String) -> Result<()> {\n    debug!("Show command:'
        'item_path={}", item_path);\n    Ok(())\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "owned_string_parameters" in result.output
    assert (
        "help: accept &str instead of String when ownership is not needed"
        in result.output
    )


def test_run_owned_string_parameters_clean(tmp_path: Path) -> None:
    """Test run passes when no owned_string_parameters violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'pub fn show(item_path: &str) -> Result<()> {\n    debug!("Show command:'
        'item_path={}", item_path);\n    Ok(())\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[owned_string_parameters]:" not in result.output
