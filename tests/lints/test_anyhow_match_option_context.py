"""Tests for the ``anyhow_match_option_context`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_match_option_context(tmp_path: Path) -> None:
    """Test run detects anyhow_match_option_context violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn example1(selected_contract: Option<Contract>, artifact: Artifact) {\n   "
        "let contract_def = match selected_contract {\n        Some(contract_def) =>"
        'contract_def,\n        None => bail!(\n            "artifact {} does not'
        'contain contract definition {}",\n            artifact.id,\n           '
        "artifact.name\n        ),\n    };\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_match_option_context" in result.output
    assert "help: use with_context on Option instead of match/bail!" in result.output


def test_run_anyhow_match_option_context_clean(tmp_path: Path) -> None:
    """Test run passes when no anyhow_match_option_context violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "fn valid1(opt: Option<i32>) -> Result<i32> {\n    let x = match opt {\n      "
        'Some(v) => v,\n        None => return Err(anyhow::anyhow!("missing")),\n   '
        "};\n    Ok(x)\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_match_option_context]:" not in result.output
