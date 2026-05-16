"""Tests for the ``underscore_in_types`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_underscore_in_types(tmp_path: Path) -> None:
    """Test run detects underscore_in_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let items: Vec<_> = values.collect();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "underscore_in_types" in result.output
    assert "help: specify the actual type instead of underscore" in result.output


def test_run_underscore_in_types_turbofish_macro(tmp_path: Path) -> None:
    """Test run detects underscore_in_types in turbofish inside macros."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        """println!(
            "{:?}",
            artifact.iter().map(|(_, n)| n).collect::<Vec<_>>()
        );\n"""
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "underscore_in_types" in result.output
    assert "help: specify the actual type instead of underscore" in result.output


def test_run_underscore_in_types_pattern_not_flagged(tmp_path: Path) -> None:
    """Test run does not flag underscore in tuple patterns."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let x = values.map(|(_, n)| n).collect::<Vec<i32>>();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[underscore_in_types]:" not in result.output


def test_run_underscore_in_types_clean(tmp_path: Path) -> None:
    """Test run passes when no underscore_in_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let items: Vec<i32> = values.collect();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[underscore_in_types]:" not in result.output
