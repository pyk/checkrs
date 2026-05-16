"""Tests for the ``panic_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_panic_usage(tmp_path: Path) -> None:
    """Test run detects panic_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'let style = match ProgressStyle::default_spinner()\n    .tick_strings(&["⠋",'
        '"⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])\n    .template("{spinner}'
        '{msg}")\n{\n    Ok(style) => style,\n    Err(e) => panic!("Failed to create'
        'spinner template: {}", e),\n};\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "panic_usage" in result.output
    assert "help: return Result instead of panicking" in result.output


def test_run_panic_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no panic_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[panic_usage]:" not in result.output
