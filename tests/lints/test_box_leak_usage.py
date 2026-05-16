"""Tests for the ``box_leak_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_box_leak_usage(tmp_path: Path) -> None:
    """Test run detects box_leak_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let db_static: &'static DatabaseConnection = Box::leak(Box::new(db));\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "box_leak_usage" in result.output
    assert "help: avoid intentional memory leaks with Box::leak" in result.output


def test_run_box_leak_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no box_leak_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let boxed = Box::new(value);\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[box_leak_usage]:" not in result.output
