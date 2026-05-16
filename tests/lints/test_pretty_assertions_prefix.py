"""Tests for the ``pretty_assertions_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_pretty_assertions_prefix(tmp_path: Path) -> None:
    """Test run detects pretty_assertions_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn test() {\n    pretty_assertions::assert_eq!(1, 2);\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "pretty_assertions_prefix" in result.output
    assert "help: import assert_eq! and use it without the prefix" in result.output


def test_run_pretty_assertions_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no pretty_assertions_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use pretty_assertions::assert_eq;\n\nfn test() {\n    assert_eq!(1, 2);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[pretty_assertions_prefix]:" not in result.output
