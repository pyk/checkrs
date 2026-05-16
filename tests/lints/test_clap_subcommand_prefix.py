"""Tests for the ``clap_subcommand_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_clap_subcommand_prefix(tmp_path: Path) -> None:
    """Test run detects clap_subcommand_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[derive(clap::Subcommand)]\nenum Commands {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "clap_subcommand_prefix" in result.output
    assert (
        "help: import Subcommand instead of using the fully qualified path"
        in result.output
    )


def test_run_clap_subcommand_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no clap_subcommand_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use clap::Subcommand;\n\n#[derive(Subcommand)]\nenum Commands {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[clap_subcommand_prefix]:" not in result.output
