"""Tests for the ``allow_unused_imports`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_allow_unused_imports(tmp_path: Path) -> None:
    """Test run detects allow_unused_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[allow(unused_imports)]\nuse std::collections::HashMap;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "allow_unused_imports" in result.output
    assert "help: remove allow(unused_imports) and clean up imports" in result.output


def test_run_allow_unused_imports_clean(tmp_path: Path) -> None:
    """Test run passes when no allow_unused_imports violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[allow(dead_code)]\nfn unused_function() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[allow_unused_imports]:" not in result.output
