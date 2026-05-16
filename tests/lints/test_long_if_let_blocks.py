"""Tests for the ``long_if_let_blocks`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_long_if_let_blocks(tmp_path: Path) -> None:
    """Test run detects long_if_let_blocks violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "if let Some(x) = foo {\n    do_a(x);\n    do_b(x);\n    do_c(x);\n   "
        "do_d(x);\n    do_e(x);\n    do_f(x);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "long_if_let_blocks" in result.output
    assert "help: refactor if let blocks longer than 5 statements" in result.output


def test_run_long_if_let_blocks_clean(tmp_path: Path) -> None:
    """Test run passes when no long_if_let_blocks violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("if let Some(x) = foo {\n    do_something(x);\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[long_if_let_blocks]:" not in result.output
