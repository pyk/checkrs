"""Tests for the ``clone_in_loops`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_clone_in_loops(tmp_path: Path) -> None:
    """Test run detects clone_in_loops violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "for i in 0..10 {\n    let x = data.clone();\n    process(x);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "clone_in_loops" in result.output
    assert "help: avoid cloning inside loops" in result.output


def test_run_clone_in_loops_clean(tmp_path: Path) -> None:
    """Test run passes when no clone_in_loops violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "let val = data.clone();\nfor i in 0..10 {\n    process(&val);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[clone_in_loops]:" not in result.output
