"""Tests for the ``use_after_mod`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_use_after_mod(tmp_path: Path) -> None:
    """Test run detects use_after_mod violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("mod agent;\nuse std::path::PathBuf;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "use_after_mod" in result.output
    assert "help: place use declarations before mod declarations" in result.output


def test_run_use_after_mod_clean(tmp_path: Path) -> None:
    """Test run passes when no use_after_mod violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use std::path::PathBuf;\nmod agent;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[use_after_mod]:" not in result.output
