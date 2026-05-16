"""Tests for the ``let_chains_in_if_let`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_let_chains_in_if_let(tmp_path: Path) -> None:
    """Test run detects let_chains_in_if_let violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("if let Some(x) = foo() {\n    process(x);\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "let_chains_in_if_let" in result.output
    assert (
        "help: use match expressions instead of let chains in if let" in result.output
    )


def test_run_let_chains_in_if_let_clean(tmp_path: Path) -> None:
    """Test run passes when no let_chains_in_if_let violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "if condition && another_condition {\n    do_something();\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[let_chains_in_if_let]:" not in result.output
