"""Tests for the ``inconsistent_example_headers`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_inconsistent_example_headers(tmp_path: Path) -> None:
    """Test run detects inconsistent_example_headers violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("/// # Example Usage\n\npub fn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "inconsistent_example_headers" in result.output
    assert "help: use '# Example' consistently" in result.output


def test_run_inconsistent_example_headers_clean(tmp_path: Path) -> None:
    """Test run passes when no inconsistent_example_headers violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("/// # Example\n\npub fn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[inconsistent_example_headers]:" not in result.output
