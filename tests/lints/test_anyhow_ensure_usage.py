"""Tests for the ``anyhow_ensure_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_ensure_usage(tmp_path: Path) -> None:
    """Test run detects anyhow_ensure_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if !index_html_path.exists() {\n    bail!("index.html not found");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "help: use ensure! instead of manual if/bail!" in result.output


def test_run_anyhow_ensure_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_ensure_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'if index_html_path.exists() {\n    bail!("index.html already exists");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_ensure_usage]:" not in result.output
