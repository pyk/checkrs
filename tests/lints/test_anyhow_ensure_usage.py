"""Tests for the ``anyhow_ensure_usage`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_anyhow_ensure_usage_negated(tmp_path: Path) -> None:
    """Test run detects negated condition with bail!."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if !index_html_path.exists() {\n'
        '    bail!("index.html not found");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output
    assert "help: use ensure! instead of manual if/bail!" in result.output


def test_run_anyhow_ensure_usage_greater_equal(tmp_path: Path) -> None:
    """Test run detects >= comparison with bail!."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "if item.calls.len() >= self.inner.max_calls_length {\n"
        '    bail!("item already contains max_calls_length calls");\n'
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output


def test_run_anyhow_ensure_usage_equal(tmp_path: Path) -> None:
    """Test run detects == comparison with bail!."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if status.code() == 0 {\n'
        '    bail!("unexpected success");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output


def test_run_anyhow_ensure_usage_not_equal_return_err(
    tmp_path: Path,
) -> None:
    """Test run detects != comparison with return Err."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if x != y {\n'
        '    return Err(anyhow::anyhow!("values do not match"));\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output


def test_run_anyhow_ensure_usage_less_than(tmp_path: Path) -> None:
    """Test run detects < comparison with bail!."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if count < 1 {\n'
        '    bail!("count must be at least 1");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output


def test_run_anyhow_ensure_usage_is_none(tmp_path: Path) -> None:
    """Test run detects .is_none() with bail!."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if item.value.is_none() {\n'
        '    bail!("value is missing");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "anyhow_ensure_usage" in result.output
    assert "1 manual if/bail! instead of ensure!" in result.output


def test_run_anyhow_ensure_usage_clean_positive(tmp_path: Path) -> None:
    """Test run passes on positive non-comparison condition."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if index_html_path.exists() {\n'
        '    bail!("index.html already exists");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_ensure_usage]:" not in result.output


def test_run_anyhow_ensure_usage_clean_no_bail(tmp_path: Path) -> None:
    """Test run passes when there is no bail! at all."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if index_html_path.exists() {\n'
        '    println!("found");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_ensure_usage]:" not in result.output


def test_run_anyhow_ensure_usage_clean_parenthesized_negation(
    tmp_path: Path,
) -> None:
    """Test run passes on parenthesized double negation."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        'if !(index_html_path.exists()) {\n'
        '    bail!("not found");\n'
        '}\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[anyhow_ensure_usage]:" not in result.output
