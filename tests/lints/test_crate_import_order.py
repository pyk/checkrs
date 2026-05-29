"""Tests for the ``crate_import_order`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_crate_import_order(tmp_path: Path) -> None:
    """Test run detects crate_import_order violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "use crate::acp::types::{AgentCapabilities, InitializeRequest};\nuse"
        "anyhow::Result;\nuse tracing::{info, warn};\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "crate_import_order" in result.output
    assert (
        "help: place crate imports after external imports,"
        " and add a blank line between external and crate imports"
        in result.output
    )


def test_run_crate_import_order_clean(tmp_path: Path) -> None:
    """Test run passes when no crate_import_order violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use anyhow::Result;\nuse tracing::{info, warn};\n\nuse"
        "crate::acp::types::{AgentCapabilities, Implementation, InitializeRequest,"
        "InitializeResponse};\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[crate_import_order]:" not in result.output
