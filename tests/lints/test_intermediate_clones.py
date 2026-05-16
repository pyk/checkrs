"""Tests for the ``intermediate_clones`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_intermediate_clones(tmp_path: Path) -> None:
    """Test run detects intermediate_clones violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn example_assign_clone_call() {\n    let params = req.params.clone();\n   "
        "process(params);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "intermediate_clones" in result.output
    assert "help: remove intermediate clone variables" in result.output


def test_run_intermediate_clones_clean(tmp_path: Path) -> None:
    """Test run passes when no intermediate_clones violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "fn example_mut_copy() {\n    let mut copy = original.clone();\n   "
        "copy.modify();\n    process(copy);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[intermediate_clones]:" not in result.output
