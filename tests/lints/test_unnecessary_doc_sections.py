"""Tests for the ``unnecessary_doc_sections`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_unnecessary_doc_sections(tmp_path: Path) -> None:
    """Test run detects unnecessary_doc_sections violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("/// # Arguments\n\npub fn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "unnecessary_doc_sections" in result.output
    assert "help: remove non-idiomatic doc comment sections" in result.output


def test_run_unnecessary_doc_sections_clean(tmp_path: Path) -> None:
    """Test run passes when no unnecessary_doc_sections violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("/// Process the input data\n\npub fn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[unnecessary_doc_sections]:" not in result.output
