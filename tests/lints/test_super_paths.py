"""Tests for the ``super_paths`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_super_paths_violation(tmp_path: Path) -> None:
    """Test run detects super_paths violations inside function bodies."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn setup() {\n"
        "    let x = super::MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[super_paths]" in result.output
    assert "1 super:: paths outside of use declarations" in result.output
    assert (
        "help: if it is a struct, import it first: in tests use `super::*`, "
        "otherwise use `use crate::module::MyStruct`"
    ) in result.output
    assert f"--> {rs}:2:" in result.output


def test_super_paths_struct_field_violation(tmp_path: Path) -> None:
    """Test run detects super_paths violations in struct fields."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "struct Foo {\n"
        "    pub panic_transactions: Vec<super::Transaction>,\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[super_paths]" in result.output
    assert "1 super:: paths outside of use declarations" in result.output
    assert f"--> {rs}:2:" in result.output


def test_super_paths_function_param_violation(tmp_path: Path) -> None:
    """Test run detects super_paths violations in function parameters."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn setup(x: super::MyStruct) {}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[super_paths]" in result.output
    assert "1 super:: paths outside of use declarations" in result.output
    assert f"--> {rs}:1:" in result.output


def test_super_paths_clean(tmp_path: Path) -> None:
    """Test run passes when no super_paths violations."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "use crate::module::MyStruct;\n"
        "\n"
        "fn setup() {\n"
        "    let x = MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[super_paths]:" not in result.output


def test_super_paths_use_inside_block_ignored(tmp_path: Path) -> None:
    """Test run ignores super:: use declarations inside blocks."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn setup() {\n"
        "    use super::MyStruct;\n"
        "    let x = MyStruct::new(target);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[super_paths]:" not in result.output
