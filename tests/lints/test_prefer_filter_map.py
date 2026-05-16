"""Tests for the ``prefer_filter_map`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_prefer_filter_map(tmp_path: Path) -> None:
    """Test run detects prefer_filter_map violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'let a = ["1", "two", "NaN", "four", "5"];\nlet mut iter = a.iter().map(|s|'
        "s.parse()).filter(|s| s.is_ok()).map(|s|"
        "s.unwrap());\nassert_eq!(iter.next(), Some(1));\nassert_eq!(iter.next(),"
        "Some(5));\nassert_eq!(iter.next(), None);\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "prefer_filter_map" in result.output
    assert "help: use filter_map instead of map().filter().map()" in result.output


def test_run_prefer_filter_map_clean(tmp_path: Path) -> None:
    """Test run passes when no prefer_filter_map violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! Clean test module.\n'
        '\n'
        'let a = ["1", "two", "NaN", "four", "5"];\nlet mut iter ='
        "a.iter().filter_map(|s| s.parse().ok());\nassert_eq!(iter.next(),"
        "Some(1));\nassert_eq!(iter.next(), Some(5));\nassert_eq!(iter.next(), None);\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[prefer_filter_map]:" not in result.output
