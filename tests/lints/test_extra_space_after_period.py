"""Tests for the ``extra_space_after_period`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_extra_space_after_period(tmp_path: Path) -> None:
    """Test run detects extra_space_after_period violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "/// A transaction can interleave multiple `vm.coinbase` calls and\n"
        "/// end on the expected address without corrupting state.  This\n"
        "/// proves the cheatcode is deterministic and safe to call.\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "extra_space_after_period" in result.output
    assert "comments with extra space after period" in result.output
    assert "help: use a single space after a period" in result.output


def test_run_extra_space_after_period_clean(tmp_path: Path) -> None:
    """Test run passes when no extra_space_after_period violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "/// A transaction can interleave multiple `vm.coinbase` calls and\n"
        "/// end on the expected address without corrupting state. This\n"
        "/// proves the cheatcode is deterministic and safe to call.\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[extra_space_after_period]:" not in result.output


def test_run_extra_space_after_period_bang(tmp_path: Path) -> None:
    """Test run detects extra space after period in inner doc comments."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Module docs.  With extra space.\n"
        "pub fn foo() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "extra_space_after_period" in result.output


def test_run_extra_space_after_period_inline(tmp_path: Path) -> None:
    """Test run detects extra space after period in inline comments."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn foo() {\n"
        "    let x = 1; // initialize.  starting at one\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "extra_space_after_period" in result.output
