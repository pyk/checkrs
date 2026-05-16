"""Tests for the ``continue_in_err_arm`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_continue_in_err_arm(tmp_path: Path) -> None:
    """Test run detects continue_in_err_arm violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let request = match request {\n    Err(e) => {\n        match optional {\n   "
        "Some(_) => continue,\n            None => e,\n        }\n    }\n    Ok(req)"
        "=> req,\n};\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "continue_in_err_arm" in result.output
    assert "help: refactor continue in Err arms to let-else" in result.output


def test_run_continue_in_err_arm_clean(tmp_path: Path) -> None:
    """Test run passes when no continue_in_err_arm violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("for item in items {\n    continue;\n}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[continue_in_err_arm]:" not in result.output
