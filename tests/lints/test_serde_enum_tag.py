"""Tests for the ``serde_enum_tag`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_serde_enum_tag(tmp_path: Path) -> None:
    """Test run detects serde_enum_tag violations on non-unit enums."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[derive(Debug, PartialEq, Clone, Deserialize)]\n"
        "pub enum Model {\n"
        "    Named { name: String },\n"
        "    Custom(String),\n"
        "}\n"
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
        "#[derive(Debug, PartialEq, Clone, Deserialize)]\n"
        "#[serde(untagged)]\n"
        "pub enum Model {\n"
        "    Named { name: String },\n"
        "    Custom(String),\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_enum_tag]:" not in result.output


def test_run_serde_enum_tag_with_tag(tmp_path: Path) -> None:
    """Test run passes when serde(tag) is present."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[derive(Deserialize)]\n"
        '#[serde(tag = "type")]\n'
        "pub enum Model {\n"
        "    Named { name: String },\n"
        "    Custom(String),\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_enum_tag]:" not in result.output


def test_run_serde_enum_tag_unit_string_enum_ok(tmp_path: Path) -> None:
    """Unit-only string enums do not need tag or untagged."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[derive(Deserialize)]\n"
        "pub enum Language {\n"
        "    Solidity,\n"
        "    Yul,\n"
        "}\n"
        "\n"
        "#[derive(Deserialize)]\n"
        '#[serde(rename_all = "camelCase")]\n'
        "pub enum StopAfter {\n"
        "    Parsing,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_enum_tag]:" not in result.output


def test_run_serde_enum_tag_attributes_are_item_scoped(tmp_path: Path) -> None:
    """Earlier item attributes must not affect later enums."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Test module.\n"
        "\n"
        "#[derive(Deserialize)]\n"
        "pub struct Earlier { x: u8 }\n"
        "\n"
        "#[derive(Deserialize)]\n"
        "pub enum Later { A, B }\n"
        "\n"
        "#[derive(Deserialize)]\n"
        "#[serde(untagged)]\n"
        "pub enum SourceContent {\n"
        "    Content { content: String },\n"
        "    Urls { urls: Vec<String> },\n"
        "}\n"
        "\n"
        "#[derive(Deserialize)]\n"
        "pub enum ShouldFlag {\n"
        "    Named { name: String },\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[serde_enum_tag]: 1 enums without serde(tag) or serde(untagged)" in (
        result.output
    )
    # Only ShouldFlag is reported (line 17 after the module doc).
    assert f"--> {rust_file}:17:1" in result.output


def test_run_serde_enum_tag_repro_solc_style(tmp_path: Path) -> None:
    """Regression: solc-rs style unit enums mixed with untagged enums."""
    rust_file = tmp_path / "standard_json_input.rs"
    rust_file.write_text(
        "#[derive(Clone, Default, Debug, Serialize, Deserialize)]\n"
        '#[serde(rename_all = "camelCase")]\n'
        "pub struct StandardJsonInput {\n"
        "    pub language: Language,\n"
        "}\n"
        "\n"
        "#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, Default)]\n"
        "pub enum Language {\n"
        "    #[default]\n"
        "    Solidity,\n"
        "    Yul,\n"
        '    #[serde(rename = "SolidityAST")]\n'
        "    SolidityAst,\n"
        '    #[serde(rename = "EVMAssembly")]\n'
        "    EvmAssembly,\n"
        "}\n"
        "\n"
        "#[derive(Clone, Debug, Serialize, Deserialize)]\n"
        "#[serde(untagged)]\n"
        "pub enum SourceContent {\n"
        "    Content { content: String },\n"
        "    Urls { urls: Vec<String> },\n"
        "}\n"
        "\n"
        "#[derive(Clone, Debug, Serialize, Deserialize)]\n"
        '#[serde(rename_all = "camelCase")]\n'
        "pub enum StopAfter {\n"
        "    Parsing,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[serde_enum_tag]:" not in result.output
