"""Tests for the ``ignored_writeln_result`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_ignored_writeln_result(tmp_path: Path) -> None:
    """Test run detects ignored_writeln_result violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "// simple ignored results should be flagged and fixed\nfn"
        "write_header(output: &mut impl std::io::Write, action: &Action) {\n    let _"
        '= writeln!(output, "### {}", action.name);\n    let _ = writeln!(output);\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "ignored_writeln_result" in result.output
    assert "help: propagate writeln! errors with `?`" in result.output


def test_run_ignored_writeln_result_clean(tmp_path: Path) -> None:
    """Test run passes when no ignored_writeln_result violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "// already using `?` to propagate errors\nfn write_header(output: &mut impl"
        "std::io::Write, action: &Action) -> std::io::Result<()> {\n   "
        'writeln!(output, "### {}", action.name)?;\n    writeln!(output)?;\n   '
        "Ok(())\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[ignored_writeln_result]:" not in result.output
