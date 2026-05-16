"""Tests for the ``serde_enum_tag`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_serde_enum_tag(tmp_path: Path) -> None:
    """Test run detects serde_enum_tag violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[derive(Debug, PartialEq, Clone, Deserialize)]\npub enum Model {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "serde_enum_tag" in result.output
    assert (
        "help: add serde(tag) or serde(untagged) to enums with Deserialize"
        in result.output
    )


def test_run_serde_enum_tag_clean(tmp_path: Path) -> None:
    """Test run passes when no serde_enum_tag violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "#[derive(Debug, PartialEq, Clone, Deserialize)]\n#[serde(untagged)]\npub enum"
        "Model {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_enum_tag]:" not in result.output
