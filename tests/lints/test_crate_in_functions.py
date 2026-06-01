"""Tests for the ``crate_in_functions`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_crate_in_functions_violation(tmp_path: Path) -> None:
    """Test run detects crate_in_functions violations."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn deploy_and_setup(contract: &Contract) -> Deployed {\n"
        "    let setup_opts ="
        " crate::evm::chain::SetupInput::new(target).calldata(setup_data);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[crate_in_functions]" in result.output
    assert "1 crate:: paths inside function bodies" in result.output
    assert (
        "help: if it is a struct, import `crate::module::MyStruct` and use "
        "`MyStruct` directly; if it is a free function, use its module "
        "directly (e.g. `crate::formatter::num` should be `formatter::num`)"
    ) in result.output
    assert f"--> {rs}:2:" in result.output


def test_crate_in_functions_clean(tmp_path: Path) -> None:
    """Test run passes when no crate_in_functions violations."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "use crate::evm::chain::SetupInput;\n"
        "\n"
        "fn deploy_and_setup(contract: &Contract) -> Deployed {\n"
        "    let setup_opts = SetupInput::new(target).calldata(setup_data);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[crate_in_functions]:" not in result.output


def test_crate_in_functions_use_inside_block_ignored(tmp_path: Path) -> None:
    """Test run ignores crate:: use declarations inside blocks."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "fn deploy_and_setup(contract: &Contract) -> Deployed {\n"
        "    use crate::evm::chain::SetupInput;\n"
        "    let setup_opts = SetupInput::new(target).calldata(setup_data);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[crate_in_functions]:" not in result.output
