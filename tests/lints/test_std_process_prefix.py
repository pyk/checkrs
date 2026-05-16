"""Tests for the ``std_process_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_process_prefix(tmp_path: Path) -> None:
    """Test run detects std_process_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn doc(crate_name: &str) -> Result<PathBuf> {\n    let mut cmd ="
        'std::process::Command::new("cargo");\n    cmd.args(["doc", "--package",'
        'crate_name, "--no-deps"]);\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_process_prefix" in result.output
    assert (
        "help: import Command instead of using the fully qualified path"
        in result.output
    )


def test_run_std_process_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_process_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::process::Command;\n\npub fn doc(crate_name: &str) -> Result<PathBuf>"
        '{\n    let mut cmd = Command::new("cargo");\n    cmd.args(["doc",'
        '"--package", crate_name, "--no-deps"]);\n}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_process_prefix]:" not in result.output
