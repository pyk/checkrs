"""Tests for the ``is_some_and_deep_match`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_is_some_and_deep_match(tmp_path: Path) -> None:
    """Test run detects is_some_and_deep_match violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "if attr\n    .path()\n    .segments\n    .last()\n    .is_some_and(|seg|"
        'seg.ident == "method") {\n    // process\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "is_some_and_deep_match" in result.output
    assert (
        "help: separate extraction and validation from is_some_and()" in result.output
    )


def test_run_is_some_and_deep_match_clean(tmp_path: Path) -> None:
    """Test run passes when no is_some_and_deep_match violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let has_last = segments.last().is_some();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[is_some_and_deep_match]:" not in result.output
