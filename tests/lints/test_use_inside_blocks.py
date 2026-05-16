"""Tests for the ``use_inside_blocks`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_use_inside_blocks(tmp_path: Path) -> None:
    """Test run detects use_inside_blocks violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "match args.command {\n    Commands::Acp => {\n        use tracing::info;\n   "
        'info!("test");\n    }\n    _ => {}\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "use_inside_blocks" in result.output
    assert "help: place use declarations at the top of the module" in result.output


def test_run_use_inside_blocks_clean(tmp_path: Path) -> None:
    """Test run passes when no use_inside_blocks violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::path::PathBuf;\nuse std::sync::Arc;\n\nfn foo() {\n    let p ="
        "PathBuf::new();\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[use_inside_blocks]:" not in result.output
