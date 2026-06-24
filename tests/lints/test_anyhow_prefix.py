"""Tests for the ``anyhow_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_prefix_bail(tmp_path: Path) -> None:
    """Test run detects anyhow::bail! violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let Some(choice) = chat_response.choices.first() else {\n   "
        'anyhow::bail!("No choices in response");\n};\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_prefix" in result.output
    assert (
        "help: import bail!/ensure! and use without the anyhow:: prefix"
        in result.output
    )


def test_run_anyhow_prefix_ensure(tmp_path: Path) -> None:
    """Test run detects anyhow::ensure! violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "anyhow::ensure!(\n"
        "    foundry_toml.exists(),\n"
        '    "not a Foundry project: {} not found",\n'
        "    foundry_toml.display()\n"
        ");\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_prefix" in result.output
    assert (
        "help: import bail!/ensure! and use without the anyhow:: prefix"
        in result.output
    )


def test_run_anyhow_prefix_clean_bail(tmp_path: Path) -> None:
    """Test run passes when bail! used without anyhow:: prefix."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use anyhow::bail;\n\nlet Some(choice) = chat_response.choices.first() else"
        '{\n    bail!("No choices in response");\n};\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_prefix]:" not in result.output


def test_run_anyhow_prefix_clean_ensure(tmp_path: Path) -> None:
    """Test run passes when ensure! used without anyhow:: prefix."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use anyhow::ensure;\n"
        "\n"
        "ensure!(\n"
        "    foundry_toml.exists(),\n"
        '    "not a Foundry project: {} not found",\n'
        "    foundry_toml.display()\n"
        ");\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_prefix]:" not in result.output
