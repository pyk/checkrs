"""Tests for the ``serde_clone_into_from_value`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_serde_clone_into_from_value(tmp_path: Path) -> None:
    """Test run detects serde_clone_into_from_value violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let p = serde_json::from_value(data.clone());\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "serde_clone_into_from_value" in result.output
    assert "help: avoid cloning before serde_json::from_value" in result.output


def test_run_serde_clone_into_from_value_clean(tmp_path: Path) -> None:
    """Test run passes when no serde_clone_into_from_value violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let p = serde_json::from_value(data);\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_clone_into_from_value]:" not in result.output
