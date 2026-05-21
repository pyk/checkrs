"""Tests for the ``std_fs_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_fs_prefix(tmp_path: Path) -> None:
    """Test run detects std_fs_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let html_content = std::fs::read_to_string(&html_path)\n    .with_context(||"
        "format!(\"failed to read file '{}'\", html_path.display()))?;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_fs_prefix" in result.output
    assert (
        "help: import `std::fs` and call functions via `fs::function_name()`"
        in result.output
    )


def test_run_std_fs_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_fs_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::fs;\n\nlet html_content = fs::read_to_string(&html_path)\n   "
        ".with_context(|| format!(\"failed to read file '{}'\","
        "html_path.display()))?;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_fs_prefix]:" not in result.output
