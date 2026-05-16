"""Tests for the ``block_doc_comments`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_block_doc_comments(tmp_path: Path) -> None:
    """Test run detects block_doc_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "/**\n * Orchestrator-only contract module for the scan command.\n *\n *"
        "Responsibilities:\n *  - Build contract-level model from an Artifact (name,"
        "natspec, storage layout).\n *  - Delegate action extraction and rendering to"
        "`contract_action` module.\n *\n * This file intentionally does NOT contain"
        "any action parsing logic.\n */\npub fn scan() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "block_doc_comments" in result.output
    assert "help: replace block doc comments with line doc comments" in result.output


def test_run_block_doc_comments_clean(tmp_path: Path) -> None:
    """Test run passes when no block_doc_comments violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "//! Contract action module.\n//!\n//! Owns the action domain model, action"
        "extraction from artifacts,\n//! NatSpec merging, and action rendering"
        "(including tracer).\n\npub fn do_something() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[block_doc_comments]:" not in result.output
