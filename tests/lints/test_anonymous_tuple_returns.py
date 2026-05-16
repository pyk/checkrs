"""Tests for the ``anonymous_tuple_returns`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anonymous_tuple_returns(tmp_path: Path) -> None:
    """Test run detects anonymous_tuple_returns violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'fn triple() -> (i32, String, bool) {\n  (42, "hello".to_string(), true)\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anonymous_tuple_returns" in result.output
    assert (
        "help: use a named struct for tuple returns with 3+ elements" in result.output
    )


def test_run_anonymous_tuple_returns_clean(tmp_path: Path) -> None:
    """Test run passes when no anonymous_tuple_returns violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn simple() -> i32 { 42 }\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anonymous_tuple_returns]:" not in result.output
