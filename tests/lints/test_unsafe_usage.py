"""Tests for the ``unsafe_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_unsafe_usage(tmp_path: Path) -> None:
    """Test run detects unsafe_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "unsafe { std::ptr::write_bytes(map_ptr, 0, crate::inspector::MAP_SIZE) };\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "unsafe_usage" in result.output
    assert "1 unsafe usage" in result.output
    assert "help: avoid unsafe code" in result.output


def test_run_unsafe_usage_fn(tmp_path: Path) -> None:
    """Test run detects unsafe fn violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "unsafe fn foo() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "unsafe_usage" in result.output
    assert "1 unsafe usage" in result.output
    assert "help: avoid unsafe code" in result.output


def test_run_unsafe_usage_clean(tmp_path: Path) -> None:
    """Test run passes when no unsafe_usage violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[unsafe_usage]:" not in result.output
