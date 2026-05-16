"""Tests for the ``scraper_element_ref_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_scraper_element_ref_prefix(tmp_path: Path) -> None:
    """Test run detects scraper_element_ref_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn should_skip_node(node: scraper::element_ref::ElementRef) -> bool {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "scraper_element_ref_prefix" in result.output
    assert (
        "help: import ElementRef instead of using the fully qualified path"
        in result.output
    )


def test_run_scraper_element_ref_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no scraper_element_ref_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use scraper::element_ref::ElementRef;\n\nfn should_skip_node(node:"
        "ElementRef) -> bool {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[scraper_element_ref_prefix]:" not in result.output
