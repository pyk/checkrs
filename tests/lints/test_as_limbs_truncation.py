"""Tests for the ``as_limbs_truncation`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_as_limbs_truncation_violation(tmp_path: Path) -> None:
    """Test run detects the as_limbs_truncation violation."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "//! Test module\n"
        "fn setup() {\n"
        "    let ts = new_state.cheatcodes.warp_timestamp;\n"
        "    new_state.block_timestamp = ts.as_limbs()[0];\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[as_limbs_truncation]:" in result.output
    assert "1 as_limbs()[0] truncates big integers" in result.output
    assert (
        "help: use `u64::try_from(val).unwrap_or(u64::MAX)` or another explicit "
        "saturating conversion instead of `.as_limbs()[0]`"
    ) in result.output


def test_as_limbs_truncation_clean(tmp_path: Path) -> None:
    """Test run passes when the file is clean."""
    rs = tmp_path / "main.rs"
    rs.write_text(
        "//! Test module\n"
        "fn setup() {\n"
        "    let ts = new_state.cheatcodes.warp_timestamp;\n"
        "    new_state.block_timestamp = u64::try_from(ts).unwrap_or(u64::MAX);\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 0
