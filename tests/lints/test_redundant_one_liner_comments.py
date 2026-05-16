"""Tests for the ``redundant_one_liner_comments`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_redundant_one_liner_comments(tmp_path: Path) -> None:
    """Test run detects redundant_one_liner_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("// Get cargo metadata\nlet metadata = cargo::metadata()?;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "redundant_one_liner_comments" in result.output
    assert "help: remove comments that merely restate the code" in result.output


def test_run_redundant_one_liner_comments_clean(tmp_path: Path) -> None:
    """Test run passes when no redundant_one_liner_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("/// This is a valid doc comment\nfn process_data() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[redundant_one_liner_comments]:" not in result.output
