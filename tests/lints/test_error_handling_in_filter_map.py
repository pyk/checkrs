"""Tests for the ``error_handling_in_filter_map`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_error_handling_in_filter_map(tmp_path: Path) -> None:
    """Test run detects error_handling_in_filter_map violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        """let params: Result<Vec<(syn::Ident, syn::Type)>, syn::Error> = inputs
    .iter()
    .filter_map(|arg| match arg {
        syn::FnArg::Receiver(_) => None,
        syn::FnArg::Typed(pat_type) => {
            let syn::Pat::Ident(pat_ident) = &*pat_type.pat else {
                return Some(Err(syn::Error::new_spanned(
                    &pat_type.pat,
                    "Expected parameter name",
                )));
            };
            Some(Ok((pat_ident.ident.clone(), (*pat_type.ty).clone())))
        }
    })
    .collect();
"""
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error_handling_in_filter_map" in result.output
    assert (
        "help: use a for loop instead of error handling in filter_map" in result.output
    )


def test_run_error_handling_in_filter_map_clean(tmp_path: Path) -> None:
    """Test run passes when no error_handling_in_filter_map violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "let result = items.iter().filter_map(|x| x.parse().ok()).collect();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[error_handling_in_filter_map]:" not in result.output
