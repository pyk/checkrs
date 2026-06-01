"""Tests for the checkrs CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_version() -> None:
    """Test --version outputs the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "checkrs 0.1.0" in result.output


def test_help() -> None:
    """Test --help shows usage information."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "checkrs" in result.output


def test_lints() -> None:
    """Test lints command lists available linters."""
    result = runner.invoke(app, ["lints"])
    assert result.exit_code == 0
    assert "mod_rs_missing_docs" in result.output
    assert "missing" in result.output


def test_run_file_not_rust(tmp_path: Path) -> None:
    """Test run rejects non-Rust files."""
    txt = tmp_path / "foo.txt"
    txt.write_text("hello")
    result = runner.invoke(app, ["run", str(txt)])
    assert result.exit_code == 1
    assert "not a Rust file" in result.output


def test_run_file_no_violations(tmp_path: Path) -> None:
    """Test run succeeds on a clean Rust file."""
    rs = tmp_path / "main.rs"
    rs.write_text("//! Clean file.\n\nfn main() {}\n")
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0


def test_run_directory(tmp_path: Path) -> None:
    """Test run traverses directories and finds violations."""
    (tmp_path / "good.rs").write_text("fn main() {}")
    (tmp_path / "sub").mkdir(parents=True)
    (tmp_path / "sub" / "mod.rs").write_text("fn foo() {}")
    result = runner.invoke(app, ["run", str(tmp_path)])
    assert result.exit_code == 1
    assert "sub/mod.rs" in result.output
    assert "help: module docs must be simple, not abstract, and direct" in result.output


def test_run_multiple_files(tmp_path: Path) -> None:
    """Test run accepts multiple Rust files."""
    a = tmp_path / "a.rs"
    b = tmp_path / "b.rs"
    a.write_text("//! Clean file.\n\nfn main() {}\n")
    b.write_text("//! Clean file.\n\nfn foo() {}\n")
    result = runner.invoke(app, ["run", str(a), str(b)])
    assert result.exit_code == 0


def test_run_multiple_directories(tmp_path: Path) -> None:
    """Test run accepts multiple directories."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / "a.rs").write_text("//! Clean file.\n\nfn main() {}\n")
    (tmp_path / "dir2" / "b.rs").write_text("//! Clean file.\n\nfn foo() {}\n")
    result = runner.invoke(app, ["run", str(tmp_path / "dir1"), str(tmp_path / "dir2")])
    assert result.exit_code == 0


def test_run_file_and_directory(tmp_path: Path) -> None:
    """Test run accepts a mix of files and directories."""
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "mod.rs").write_text("fn foo() {}")
    (tmp_path / "main.rs").write_text("fn main() {}")
    result = runner.invoke(
        app,
        ["run", str(tmp_path / "main.rs"), str(tmp_path / "dir")],
    )
    assert result.exit_code == 1
    assert "dir/mod.rs" in result.output
    assert "help: module docs must be simple, not abstract, and direct" in result.output


def test_run_suppression_same_line(tmp_path: Path) -> None:
    """Test same-line suppression comment."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "unsafe { std::ptr::write_bytes(map_ptr, 0, 1024) };"
        " // checkrs: allow(unsafe_usage)\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0
    assert "note[unsafe_usage]: 1 unsafe usage ignored" in result.output


def test_run_suppression_previous_line(tmp_path: Path) -> None:
    """Test previous-line suppression comment."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "// checkrs: allow(unsafe_usage)\n"
        "unsafe { std::ptr::write_bytes(map_ptr, 0, 1024) };\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0
    assert "note[unsafe_usage]: 1 unsafe usage ignored" in result.output


def test_run_suppression_ignore_all(tmp_path: Path) -> None:
    """Test ignore suppression comment."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "unsafe { std::ptr::write_bytes(map_ptr, 0, 1024) };"
        " // checkrs: ignore\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0
    assert "note[unsafe_usage]: 1 unsafe usage ignored" in result.output
