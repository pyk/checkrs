"""Tests for the ``revm_primitives_bytes_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_revm_primitives_bytes_prefix(tmp_path: Path) -> None:
    """Test run detects revm_primitives_bytes_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "let vm_code = revm::bytecode::Bytecode::new_raw(\n"
        "    revm::primitives::Bytes::from_static(&[0x00]),\n"
        ");\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "revm_primitives_bytes_prefix" in result.output
    assert (
        "help: import Bytes and use it without the revm::primitives:: prefix"
        in result.output
    )


def test_run_revm_primitives_bytes_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no revm_primitives_bytes_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::primitives::Bytes;\n\n"
        "let vm_code = Bytecode::new_raw(Bytes::from_static(&[0x00]));\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[revm_primitives_bytes_prefix]:" not in result.output


def test_run_revm_primitives_bytes_prefix_use_statement_allowed(
    tmp_path: Path,
) -> None:
    """Test that import statements are not flagged."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::primitives::Bytes;\n\n"
        "let vm_code = Bytecode::new_raw(Bytes::from_static(&[0x00]));\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 0
    assert "error[revm_primitives_bytes_prefix]:" not in result.output
