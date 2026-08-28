"""Tests for the ``bool_assert_comparison`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_bool_assert_comparison(tmp_path: Path) -> None:
    """Test run detects bool_assert_comparison violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn f() { assert_eq!(x > 0, true); }\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "bool_assert_comparison" in result.output
    assert (
        "help: use `assert!(...)` instead of `assert_eq!` with `true`/`false`"
        in result.output
    )


def test_run_bool_assert_comparison_true_first(tmp_path: Path) -> None:
    """Test detects when true is first argument."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn f() { assert_eq!(true, x > 0); }\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "bool_assert_comparison" in result.output


def test_run_bool_assert_comparison_false(tmp_path: Path) -> None:
    """Test detects false literal."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn f() { assert_eq!(x, false); }\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "bool_assert_comparison" in result.output


def test_run_bool_assert_comparison_ne(tmp_path: Path) -> None:
    """Test detects assert_ne with bool."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("fn f() { assert_ne!(x, true); }\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "bool_assert_comparison" in result.output


def test_run_bool_assert_comparison_with_msg(tmp_path: Path) -> None:
    """Test detects with format message."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('fn f() { assert_eq!(x, true, "msg"); }\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "bool_assert_comparison" in result.output


def test_run_bool_assert_comparison_clean(tmp_path: Path) -> None:
    """Test run passes when no bool_assert_comparison violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "fn f() { assert!(x > 0); }\n"
        "fn g() { assert_eq!(a, b); }\n"
        "fn h() { assert_ne!(a, b); }\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[bool_assert_comparison]:" not in result.output
