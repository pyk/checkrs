"""Tests for the ``revm_database_cachedb_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_revm_database_cachedb_prefix(tmp_path: Path) -> None:
    """Test run detects revm_database_cachedb_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn create_db() -> revm::database::CacheDB<InMemoryDB> {\n"
        "    // ...\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "revm_database_cachedb_prefix" in result.output
    assert (
        "help: import CacheDB and use it without the revm::database:: prefix"
        in result.output
    )


def test_run_revm_database_cachedb_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no revm_database_cachedb_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::database::CacheDB;\n\n"
        "pub fn create_db() -> CacheDB<InMemoryDB> {\n"
        "    // ...\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[revm_database_cachedb_prefix]:" not in result.output
