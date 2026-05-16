"""Tests for the ``nested_if_let`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_nested_if_let(tmp_path: Path) -> None:
    """Test run detects nested_if_let violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "if let Some(a) = foo {\n    if let Some(b) = bar {\n        process(a, b);\n "
        "}\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "nested_if_let" in result.output
    assert "help: use match or and_then instead of nested if let" in result.output


def test_run_nested_if_let_clean(tmp_path: Path) -> None:
    """Test run passes when no nested_if_let violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("if let Some(x) = foo {\n    do_something(x);\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[nested_if_let]:" not in result.output
