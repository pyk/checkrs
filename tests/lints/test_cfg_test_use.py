"""Tests for the ``cfg_test_use`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_cfg_test_use_violation(tmp_path: Path) -> None:
    """Test run detects the cfg_test_use violation."""
    rs = tmp_path / "main.rs"
    rs.write_text("#[cfg(test)]\nuse std::io::Write;\n")
    result = runner.invoke(app, ["run", str(rs)])
    assert result.exit_code == 1
    assert "error[cfg_test_use]" in result.output
    assert "1 using #[cfg(test)] outside mod tests" in result.output
    assert "help: place #[cfg(test)] only before mod tests" in result.output


def test_cfg_test_use_clean(tmp_path: Path) -> None:
    """Test run passes when #[cfg(test)] is followed by mod tests."""
    rs = tmp_path / "main.rs"
    rs.write_text("#[cfg(test)]\nmod tests {\n}\n")
    result = runner.invoke(app, ["run", str(rs)])
    assert "error[cfg_test_use]:" not in result.output
