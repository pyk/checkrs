"""Tests for the ``std_hashset_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_hashset_prefix(tmp_path: Path) -> None:
    """Test run detects std_hashset_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let set = std::collections::HashSet::new();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_hashset_prefix" in result.output
    assert (
        "help: import HashSet instead of using the fully qualified path"
        in result.output
    )


def test_run_std_hashset_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_hashset_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::collections::HashSet;\n\nlet set = HashSet::new();\nlet set2:"
        "HashSet<String> = HashSet::new();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_hashset_prefix]:" not in result.output
