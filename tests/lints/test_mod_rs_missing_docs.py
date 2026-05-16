"""Tests for the ``mod_rs_missing_docs`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_mod_rs_missing_docs(tmp_path: Path) -> None:
    """Test run detects missing mod.rs documentation."""
    mod_rs = tmp_path / "mod.rs"
    mod_rs.write_text("fn main() {}")
    result = runner.invoke(app, ["run", str(mod_rs)])
    assert result.exit_code == 1
    assert "mod_rs_missing_docs" in result.output
    assert "help: module docs must be simple, not abstract, and direct" in result.output


def test_run_mod_rs_with_docs(tmp_path: Path) -> None:
    """Test run passes when mod.rs has documentation."""
    mod_rs = tmp_path / "mod.rs"
    mod_rs.write_text("//! This module does stuff.\n\nfn main() {}\n")
    result = runner.invoke(app, ["run", str(mod_rs)])
    assert "error[mod_rs_missing_docs]:" not in result.output
