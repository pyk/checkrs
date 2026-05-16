"""Tests for the checkrs CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_version() -> None:
    """Test --version outputs the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "checkrs 0.1.0" in result.output


def test_help() -> None:
    """Test --help shows usage information."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "checkrs" in result.output


def test_lints() -> None:
    """Test lints command lists available linters."""
    result = runner.invoke(app, ["lints"])
    assert result.exit_code == 0
    assert "mod_rs_missing_docs" in result.output


def test_run_file_not_rust(tmp_path: Path) -> None:
    """Test run rejects non-Rust files."""
    txt = tmp_path / "foo.txt"
    txt.write_text("hello")
    result = runner.invoke(app, ["run", str(txt)])
    assert result.exit_code == 1
    assert "not a Rust file" in result.output


def test_run_file_no_violations(tmp_path: Path) -> None:
    """Test run succeeds on a clean Rust file."""
    rs = tmp_path / "main.rs"
    rs.write_text("fn main() {}")
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0


def test_run_directory(tmp_path: Path) -> None:
    """Test run traverses directories and finds violations."""
    (tmp_path / "good.rs").write_text("fn main() {}")
    (tmp_path / "sub").mkdir(parents=True)
    (tmp_path / "sub" / "mod.rs").write_text("fn foo() {}")
    result = runner.invoke(app, ["run", str(tmp_path)])
    assert result.exit_code == 1
    assert "sub/mod.rs" in result.output
