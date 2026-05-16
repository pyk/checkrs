"""Tests for the ``<lint_name>`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_<lint_name>_violation(tmp_path: Path) -> None:
    """Test run detects the <lint_name> violation."""
    rs = tmp_path / "main.rs"
    rs.write_text("<code that triggers the lint>")
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[<lint_name>]" in result.output
    assert "1 <description>" in result.output
    assert "help: <help text>" in result.output


def test_<lint_name>_clean(tmp_path: Path) -> None:
    """Test run passes when the file is clean."""
    rs = tmp_path / "main.rs"
    rs.write_text("<code that does not trigger the lint>")
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0
