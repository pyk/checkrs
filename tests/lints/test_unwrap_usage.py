"""Tests for the ``unwrap_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_unwrap_usage(tmp_path: Path) -> None:
    """Test run detects unwrap_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let x = option.unwrap();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "unwrap_usage" in result.output
    assert (
        "help: use `?` or explicit error handling instead of unwrap()" in result.output
    )


def test_run_unwrap_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no unwrap_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[test]\nfn it_works() {\n    let x = option.unwrap();\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[unwrap_usage]:" not in result.output
