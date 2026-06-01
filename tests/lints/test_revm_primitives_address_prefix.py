"""Tests for the ``revm_primitives_address_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_revm_primitives_address_prefix(tmp_path: Path) -> None:
    """Test run detects revm_primitives_address_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "struct Deployed {\n"
        "    chain: Chain,\n"
        "    address: revm::primitives::Address,\n"
        "    runtime_code: Bytes,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "revm_primitives_address_prefix" in result.output
    assert (
        "help: import Address and use it without the revm::primitives:: prefix"
        in result.output
    )


def test_run_revm_primitives_address_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no revm_primitives_address_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::primitives::Address;\n\n"
        "struct Deployed {\n"
        "    chain: Chain,\n"
        "    address: Address,\n"
        "    runtime_code: Bytes,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[revm_primitives_address_prefix]:" not in result.output


def test_run_revm_primitives_address_prefix_use_statement_allowed(
    tmp_path: Path,
) -> None:
    """Test that import statements are not flagged."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use revm::primitives::Address;\n"
        "use revm::primitives::{Address, Bytes};\n\n"
        "struct Deployed {\n"
        "    chain: Chain,\n"
        "    address: Address,\n"
        "    runtime_code: Bytes,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 0
    assert "error[revm_primitives_address_prefix]:" not in result.output
