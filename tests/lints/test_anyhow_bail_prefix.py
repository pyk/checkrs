"""Tests for the ``anyhow_bail_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_bail_prefix(tmp_path: Path) -> None:
    """Test run detects anyhow_bail_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let Some(choice) = chat_response.choices.first() else {\n   "
        'anyhow::bail!("No choices in response");\n};\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_bail_prefix" in result.output
    assert "help: import bail! and use it without the anyhow:: prefix" in result.output


def test_run_anyhow_bail_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_bail_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use anyhow::bail;\n\nlet Some(choice) = chat_response.choices.first() else"
        '{\n    bail!("No choices in response");\n};\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_bail_prefix]:" not in result.output
