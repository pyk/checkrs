"""Tests for the ``immediately_invoked_closures`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_immediately_invoked_closures(tmp_path: Path) -> None:
    """Test run detects immediately_invoked_closures violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let result: Result<()> = (|| {\n    Ok(())\n})();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "immediately_invoked_closures" in result.output
    assert (
        "help: define a named function instead of immediately-invoked closures"
        in result.output
    )


def test_run_immediately_invoked_closures_clean(tmp_path: Path) -> None:
    """Test run passes when no immediately_invoked_closures violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "fn my_function() -> Result<()> {\n    Ok(())\n}\n\nlet result ="
        "my_function();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[immediately_invoked_closures]:" not in result.output
