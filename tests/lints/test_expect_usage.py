"""Tests for the ``expect_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_expect_usage(tmp_path: Path) -> None:
    """Test run detects expect_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'fn main() {\n    let x = file.open().expect("file should exist");\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "expect_usage" in result.output
    assert (
        "help: use `?` or explicit error handling instead of expect()" in result.output
    )


def test_run_expect_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no expect_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "mod tests {\n    #[test]\n    fn it_works() {\n        let x ="
        'file.open().expect("file should exist");\n    }\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[expect_usage]:" not in result.output
