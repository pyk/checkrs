"""Tests for the ``path_param_types`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_path_param_types(tmp_path: Path) -> None:
    """Test run detects path_param_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn new(session_id: u64, project_path: &str, model: &str) -> Self {\n   "
        "Self { session_id, project_path: project_path.into(), model }\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "path_param_types" in result.output
    assert "help: use impl AsRef<Path> for path-related parameters" in result.output


def test_run_path_param_types_clean(tmp_path: Path) -> None:
    """Test run passes when no path_param_types violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "pub fn new(session_id: u64, project_path: impl AsRef<Path>, model: &str) ->"
        "Self {\n    Self { session_id, project_path:"
        "project_path.as_ref().to_path_buf(), model }\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[path_param_types]:" not in result.output
