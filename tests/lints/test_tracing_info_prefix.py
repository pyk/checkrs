"""Tests for the ``tracing_info_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_tracing_info_prefix(tmp_path: Path) -> None:
    """Test run detects tracing_info_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::info!("message");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_info_prefix" in result.output
    assert "help: import info! and use it without the tracing:: prefix" in result.output


def test_run_tracing_info_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no tracing_info_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'use tracing::info;\n\ninfo!("message");\nlet value = 42;\ninfo!("value is'
        '{}", value);\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[tracing_info_prefix]:" not in result.output
