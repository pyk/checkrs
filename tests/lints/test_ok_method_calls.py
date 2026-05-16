"""Tests for the ``ok_method_calls`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_ok_method_calls(tmp_path: Path) -> None:
    """Test run detects ok_method_calls violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("attr.parse_args::<syn::LitStr>().map(|s| s.value()).ok()\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "ok_method_calls" in result.output
    assert "help: propagate errors with `?` instead of ok()" in result.output


def test_run_ok_method_calls_clean(tmp_path: Path) -> None:
    """Test run passes when no ok_method_calls violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let x = file.open()?;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[ok_method_calls]:" not in result.output
