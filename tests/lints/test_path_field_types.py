"""Tests for the ``path_field_types`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_path_field_types(tmp_path: Path) -> None:
    """Test run detects path_field_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub struct Session {\n    pub project_path: String,\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "path_field_types" in result.output
    assert "help: use PathBuf for path-related struct fields" in result.output


def test_run_path_field_types_clean(tmp_path: Path) -> None:
    """Test run passes when no path_field_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("pub struct Session {\n    pub project_path: PathBuf,\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[path_field_types]:" not in result.output
