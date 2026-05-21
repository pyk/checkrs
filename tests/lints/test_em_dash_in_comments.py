"""Tests for the ``em_dash_in_comments`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_em_dash_in_comments(tmp_path: Path) -> None:
    """Test run detects em_dash_in_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Foundry integration for compiling Solidity projects.\n"
        "//!\n"
        "//! 1. Building a project — compile via `forge build`.\n"
        "//! 2. Loading build artifacts — read from `out/` directory.\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "em_dash_in_comments" in result.output
    assert "comments with em dash" in result.output
    assert "help: replace em dash with a colon or hyphen" in result.output


def test_run_em_dash_in_comments_clean(tmp_path: Path) -> None:
    """Test run passes when no em_dash_in_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Foundry integration for compiling Solidity projects.\n"
        "//!\n"
        "//! 1. Building a project - compile via `forge build`.\n"
        "//! 2. Loading build artifacts - read from `out/` directory.\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[em_dash_in_comments]:" not in result.output


def test_run_em_dash_in_comments_block(tmp_path: Path) -> None:
    """Test run detects em dash inside block comments."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "/*\n"
        " * Building a project — compile via `forge build`.\n"
        " */\n"
        "pub fn foo() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "em_dash_in_comments" in result.output


def test_run_em_dash_in_comments_inline(tmp_path: Path) -> None:
    """Test run detects em dash inside inline comments."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn foo() {\n"
        "    let x = 1; // initialize counter — starting at one\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "em_dash_in_comments" in result.output
