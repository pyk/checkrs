"""Tests for the ``comment_banner`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_comment_banner(tmp_path: Path) -> None:
    """Test run detects comment_banner violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "// ---- Lightweight ID extraction ----\n"
        "pub fn extract_id(input: &str) -> Option<u64> {\n"
        "    None\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[comment_banner]: 1 comment banner" in result.output
    assert f"--> {rust_file}:3:1" in result.output
    assert "help: remove banner-style divider comments" in result.output


def test_run_comment_banner_clean(tmp_path: Path) -> None:
    """Test run passes when no comment_banner violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "// identifier extraction\n"
        "pub fn extract_id(input: &str) -> Option<u64> {\n"
        "    None\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 0
    assert "error[comment_banner]:" not in result.output
