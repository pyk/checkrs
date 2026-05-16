"""Tests for the ``self_imports`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_self_imports(tmp_path: Path) -> None:
    """Test run detects self_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use self::Something;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "self_imports" in result.output
    assert "help: import items directly instead of using self::" in result.output


def test_run_self_imports_clean(tmp_path: Path) -> None:
    """Test run passes when no self_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use crate::module::Something;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[self_imports]:" not in result.output
