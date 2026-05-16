"""Tests for the ``std_import_order`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_import_order(tmp_path: Path) -> None:
    """Test run detects std_import_order violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "use anyhow::Result;\nuse clap::Parser;\nuse clap::Subcommand;\nuse"
        "clap_verbosity_flag::Verbosity;\nuse std::path::PathBuf;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_import_order" in result.output
    assert "help: place std imports before external and crate imports" in result.output


def test_run_std_import_order_clean(tmp_path: Path) -> None:
    """Test run passes when no std_import_order violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::path::PathBuf;\nuse std::collections::HashMap;\n\nuse"
        "anyhow::Result;\nuse clap::Parser;\nuse clap_verbosity_flag::Verbosity;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_import_order]:" not in result.output
