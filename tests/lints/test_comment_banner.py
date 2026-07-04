"""Tests for the ``comment_banner`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()

_DASHES = "-" * 50


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


def test_run_comment_banner_three_line(tmp_path: Path) -> None:
    """Test run detects a three-line banner divider."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        f"// {_DASHES}\n"
        "// Tests\n"
        f"// {_DASHES}\n"
        "pub fn extract_id(input: &str) -> Option<u64> {\n"
        "    None\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[comment_banner]: 1 comment banner" in result.output
    assert f"--> {rust_file}:3:1" in result.output
    assert "help: remove banner-style divider comments" in result.output


def test_run_comment_banner_classification(tmp_path: Path) -> None:
    """Test run detects a classification banner divider."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        f"// {_DASHES}\n"
        "// Classification: turn a content line into an mdast node.\n"
        f"// {_DASHES}\n"
        "pub fn convert(input: &str) -> Option<u64> {\n"
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


def test_run_comment_banner_no_false_positive_dash_only(tmp_path: Path) -> None:
    """Test run passes when dash-only lines do not form a banner."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        f"// {_DASHES}\n"
        f"// {_DASHES}\n"
        "pub fn extract_id(input: &str) -> Option<u64> {\n"
        "    None\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 0
    assert "error[comment_banner]:" not in result.output
