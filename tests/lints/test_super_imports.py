"""Tests for the ``super_imports`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_super_imports(tmp_path: Path) -> None:
    """Test run detects super_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use super::Something;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "super_imports" in result.output
    assert "help: import items directly instead of using super::" in result.output


def test_run_super_imports_clean(tmp_path: Path) -> None:
    """Test run passes when no super_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use crate::module::Something;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[super_imports]:" not in result.output
