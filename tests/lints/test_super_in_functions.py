"""Tests for the ``super_in_functions`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_super_in_functions_violation(tmp_path: Path) -> None:
    """Test run detects super_in_functions violations."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn setup() {\n"
        "    let x = super::MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[super_in_functions]" in result.output
    assert "1 super:: paths inside function bodies" in result.output
    assert (
        "help: if it is a struct, import it first: in tests use `super::*`, "
        "otherwise use `use crate::module::MyStruct`"
    ) in result.output
    assert f"--> {rs}:2:" in result.output


def test_super_in_functions_clean(tmp_path: Path) -> None:
    """Test run passes when no super_in_functions violations."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "use crate::module::MyStruct;\n"
        "\n"
        "fn setup() {\n"
        "    let x = MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[super_in_functions]:" not in result.output


def test_super_in_functions_use_inside_block_ignored(tmp_path: Path) -> None:
    """Test run ignores super:: use declarations inside blocks."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn setup() {\n"
        "    use super::MyStruct;\n"
        "    let x = MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[super_in_functions]:" not in result.output
