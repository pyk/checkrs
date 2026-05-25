"""Tests for the ``revm_bytecode_bytecode_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_revm_bytecode_bytecode_prefix(tmp_path: Path) -> None:
    """Test run detects revm_bytecode_bytecode_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let vm_code = revm::bytecode::Bytecode::new_raw(\n"
        "    revm::primitives::Bytes::from_static(&[0x00]),\n"
        ");\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "revm_bytecode_bytecode_prefix" in result.output
    assert (
        "help: import Bytecode and use it without the revm::bytecode:: prefix"
        in result.output
    )


def test_run_revm_bytecode_bytecode_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no revm_bytecode_bytecode_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::bytecode::Bytecode;\n\n"
        "let vm_code = Bytecode::new_raw(Bytes::from_static(&[0x00]));\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[revm_bytecode_bytecode_prefix]:" not in result.output


def test_run_revm_bytecode_bytecode_prefix_use_statement_allowed(
    tmp_path: Path,
) -> None:
    """Test that import statements are not flagged."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::bytecode::Bytecode;\n\n"
        "let vm_code = Bytecode::new_raw(Bytes::from_static(&[0x00]));\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 0
    assert "error[revm_bytecode_bytecode_prefix]:" not in result.output
