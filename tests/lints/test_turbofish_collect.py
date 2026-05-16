"""Tests for the ``turbofish_collect`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_turbofish_collect(tmp_path: Path) -> None:
    """Test run detects turbofish_collect violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let text = element.text().collect::<String>();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "turbofish_collect" in result.output
    assert (
        "help: use a type annotation instead of turbofish with collect()"
        in result.output
    )


def test_run_turbofish_collect_clean(tmp_path: Path) -> None:
    """Test run passes when no turbofish_collect violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("let text: String = element.text().collect();\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[turbofish_collect]:" not in result.output
