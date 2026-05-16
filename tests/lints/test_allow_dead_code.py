"""Tests for the ``allow_dead_code`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_allow_dead_code(tmp_path: Path) -> None:
    """Test run detects allow_dead_code violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[allow(dead_code)]\nfn unused_function() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "allow_dead_code" in result.output
    assert "help: remove allow(dead_code) and refactor unused code" in result.output


def test_run_allow_dead_code_clean(tmp_path: Path) -> None:
    """Test run passes when no allow_dead_code violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[allow(unused_imports)]\nfn used_function() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[allow_dead_code]:" not in result.output
