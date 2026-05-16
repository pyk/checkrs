"""Tests for the ``must_use_attribute`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_must_use_attribute(tmp_path: Path) -> None:
    """Test run detects must_use_attribute violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[must_use]\npub fn new() -> Self {\n    Self { min_score: 5 }\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "must_use_attribute" in result.output
    assert "help: remove must_use attributes" in result.output


def test_run_must_use_attribute_clean(tmp_path: Path) -> None:
    """Test run passes when no must_use_attribute violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[allow(dead_code)]\npub fn unused() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[must_use_attribute]:" not in result.output
