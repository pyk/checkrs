"""Tests for the ``clone_in_iterator`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_clone_in_iterator(tmp_path: Path) -> None:
    """Test run detects clone_in_iterator violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let result: Vec<_> = items.iter().map(|item| item.clone()).collect();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "clone_in_iterator" in result.output
    assert "help: avoid cloning inside iterator methods" in result.output


def test_run_clone_in_iterator_clean(tmp_path: Path) -> None:
    """Test run passes when no clone_in_iterator violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "let item = data.clone();\nlet result: Vec<_> = items.iter().map(|x|"
        "item).collect();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[clone_in_iterator]:" not in result.output
