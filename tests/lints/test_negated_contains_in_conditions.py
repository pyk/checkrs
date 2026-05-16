"""Tests for the ``negated_contains_in_conditions`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_negated_contains_in_conditions(tmp_path: Path) -> None:
    """Test run detects negated_contains_in_conditions violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("if !list.contains(&x) {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "negated_contains_in_conditions" in result.output
    assert "help: extract negated contains() to a named variable" in result.output


def test_run_negated_contains_in_conditions_clean(tmp_path: Path) -> None:
    """Test run passes when no negated_contains_in_conditions violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("if crate_not_exists {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[negated_contains_in_conditions]:" not in result.output
