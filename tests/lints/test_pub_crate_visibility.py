"""Tests for the ``pub_crate_visibility`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_pub_crate_visibility_violation(tmp_path: Path) -> None:
    """Test run detects pub_crate_visibility violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub(crate) struct Foo;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[pub_crate_visibility]" in result.output
    assert "1 pub(crate) visibility modifier" in result.output
    assert "help: use `pub` instead of `pub(crate)`" in result.output


def test_pub_crate_visibility_clean(tmp_path: Path) -> None:
    """Test run passes when no pub(crate) visibility."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub struct Foo;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[pub_crate_visibility]" not in result.output


def test_pub_crate_visibility_on_field(tmp_path: Path) -> None:
    """Test run detects pub(crate) on struct fields."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub struct IssueCount {\n"
        "    pub(crate) severity: String,\n"
        "    pub count: u32,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[pub_crate_visibility]" in result.output
    assert "1 pub(crate) visibility modifier" in result.output


def test_pub_crate_visibility_skips_pub_super(tmp_path: Path) -> None:
    """Test run does not flag pub(super)."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub(super) fn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[pub_crate_visibility]" not in result.output
