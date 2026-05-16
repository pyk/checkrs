"""Tests for the ``match_panic_to_let_else`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_match_panic_to_let_else(tmp_path: Path) -> None:
    """Test run detects match_panic_to_let_else violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "match event {\n    MessageStreamEvent::ContentBlockStop(e) => {\n       "
        'assert_eq!(e.index, 0);\n    }\n    _ => panic!("Expected ContentBlockStop'
        'event"),\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "match_panic_to_let_else" in result.output
    assert "help: refactor match with panic catch-all to let-else" in result.output


def test_run_match_panic_to_let_else_clean(tmp_path: Path) -> None:
    """Test run passes when no match_panic_to_let_else violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "match event {\n    MessageStreamEvent::ContentBlockStop(e) => {\n       "
        "handle(e);\n    }\n    MessageStreamEvent::ContentBlockStart(e) => {\n       "
        "handle_other(e);\n    }\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[match_panic_to_let_else]:" not in result.output
