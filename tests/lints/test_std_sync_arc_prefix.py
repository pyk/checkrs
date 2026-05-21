"""Tests for the ``std_sync_arc_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_sync_arc_prefix(tmp_path: Path) -> None:
    """Test run detects std_sync_arc_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let rpc = std::sync::Arc::new(client);\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_sync_arc_prefix" in result.output
    assert (
        "help: import Arc instead of using the fully qualified path"
        in result.output
    )


def test_run_std_sync_arc_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_sync_arc_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::sync::Arc;\n\n"
        "let rpc = Arc::new(client);\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_sync_arc_prefix]:" not in result.output
