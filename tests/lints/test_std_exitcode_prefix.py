"""Tests for the ``std_exitcode_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_exitcode_prefix(tmp_path: Path) -> None:
    """Test run detects std_exitcode_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn main() {\n"
        "    std::process::ExitCode::SUCCESS\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_exitcode_prefix" in result.output
    assert (
        "help: import ExitCode instead of using the fully qualified path"
        in result.output
    )


def test_run_std_exitcode_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_exitcode_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "use std::process::ExitCode;\n\n"
        "fn main() {\n"
        "    ExitCode::SUCCESS\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_exitcode_prefix]:" not in result.output
