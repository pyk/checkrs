"""Tests for the ``parking_lot_rwlock`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_parking_lot_rwlock_fully_qualified(tmp_path: Path) -> None:
    """Test run detects fully qualified parking_lot::RwLock."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn get_lock() -> parking_lot::RwLock<String> {\n"
        "    parking_lot::RwLock::new(String::new())\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "parking_lot_rwlock" in result.output
    assert (
        "2 parking_lot::RwLock used with fully qualified path" in result.output
    )
    assert (
        "help: import RwLock and use it without the parking_lot:: prefix"
        in result.output
    )


def test_run_parking_lot_rwlock_imported(tmp_path: Path) -> None:
    """Test run passes when RwLock is imported from parking_lot."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "use parking_lot::RwLock;\n"
        "\n"
        "pub fn get_lock() -> RwLock<String> {\n"
        "    RwLock::new(String::new())\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[parking_lot_rwlock]:" not in result.output


def test_run_parking_lot_rwlock_clean(tmp_path: Path) -> None:
    """Test run passes when no parking_lot::RwLock prefix is used."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "use std::sync::RwLock;\n"
        "\n"
        "pub fn get_lock() -> RwLock<String> {\n"
        "    RwLock::new(String::new())\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[parking_lot_rwlock]:" not in result.output


def test_run_parking_lot_rwlock_read_guard_not_flagged(tmp_path: Path) -> None:
    """Test run does not flag parking_lot::RwLockReadGuard."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("use parking_lot::RwLockReadGuard;\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[parking_lot_rwlock]:" not in result.output
