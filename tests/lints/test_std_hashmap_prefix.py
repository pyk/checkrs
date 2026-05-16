"""Tests for the ``std_hashmap_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_std_hashmap_prefix(tmp_path: Path) -> None:
    """Test run detects std_hashmap_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "pub fn get_config() -> Result<std::collections::HashMap<String, String>> {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "std_hashmap_prefix" in result.output
    assert (
        "help: import HashMap instead of using the fully qualified path"
        in result.output
    )


def test_run_std_hashmap_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no std_hashmap_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use std::collections::HashMap;\n\nlet map = HashMap::new();\nlet config:"
        "HashMap<String, String> = HashMap::new();\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[std_hashmap_prefix]:" not in result.output
