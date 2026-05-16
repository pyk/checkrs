"""Tests for the ``prefer_module_imports`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_prefer_module_imports(tmp_path: Path) -> None:
    """Test run detects prefer_module_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use crate::session::SessionManager;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "prefer_module_imports" in result.output
    assert "help: import the module instead of specific items" in result.output


def test_run_prefer_module_imports_clean(tmp_path: Path) -> None:
    """Test run passes when no prefer_module_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use crate::providers::zai;\nuse crate::session;\nuse crate::ui;\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[prefer_module_imports]:" not in result.output
