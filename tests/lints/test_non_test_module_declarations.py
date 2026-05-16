"""Tests for the ``non_test_module_declarations`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_non_test_module_declarations(tmp_path: Path) -> None:
    """Test run detects non_test_module_declarations violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("mod builder {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "non_test_module_declarations" in result.output
    assert "help: move non-test modules to separate files" in result.output


def test_run_non_test_module_declarations_clean(tmp_path: Path) -> None:
    """Test run passes when no non_test_module_declarations violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("mod tests {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[non_test_module_declarations]:" not in result.output
