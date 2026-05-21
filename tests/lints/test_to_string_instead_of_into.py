"""Tests for the ``to_string_instead_of_into`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_to_string_instead_of_into(tmp_path: Path) -> None:
    """Test run detects to_string_instead_of_into violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let s = value.to_string();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "to_string_instead_of_into" in result.output
    assert "help: use into() instead of to_string() when possible" in result.output


def test_run_to_string_instead_of_into_clean(tmp_path: Path) -> None:
    """Test run passes when no to_string_instead_of_into violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('let s: String = "hello".into();\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[to_string_instead_of_into]:" not in result.output


def test_run_to_string_in_join_allowed(tmp_path: Path) -> None:
    """Test run allows to_string inside Path::join arguments."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn main() {\n    self.base_dir.join(self.chain_id.to_string());\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[to_string_instead_of_into]:" not in result.output
