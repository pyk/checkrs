"""Tests for the ``tracing_prefix`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_tracing_prefix_info(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for info."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::info!("message");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::info! with prefix" in result.output
    assert (
        "help: import `tracing` items and use them without the `tracing::` prefix"
        in result.output
    )


def test_run_tracing_prefix_error(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for error."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::error!("{err:#}");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::error! with prefix" in result.output


def test_run_tracing_prefix_warn(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for warn."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::warn!("warn");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::warn! with prefix" in result.output


def test_run_tracing_prefix_debug(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for debug."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::debug!("debug");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::debug! with prefix" in result.output


def test_run_tracing_prefix_trace(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for trace."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text('tracing::trace!("trace");\n')
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::trace! with prefix" in result.output


def test_run_tracing_prefix_instrument(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for instrument."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[tracing::instrument]\nfn foo() {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::instrument with prefix" in result.output


def test_run_tracing_prefix_instrument_with_args(tmp_path: Path) -> None:
    """Test run detects tracing_prefix violations for instrument with args."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text("#[tracing::instrument(skip(arg))]\nfn foo(arg: i32) {}\n")
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::instrument with prefix" in result.output


def test_run_tracing_prefix_user_snippet(tmp_path: Path) -> None:
    """Test run detects original user snippet with error."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "fn main() {\n"
        "    if let Err(err) = cli.run() {\n"
        '        tracing::error!("{err:#}");\n'
        "        std::process::exit(1);\n"
        "    }\n"
        "}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "tracing_prefix" in result.output
    assert "tracing::error! with prefix" in result.output
    assert "1 tracing:: with prefix" in result.output


def test_run_tracing_prefix_clean(tmp_path: Path) -> None:
    """Test run passes when no tracing_prefix violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        'use tracing::info;\n\ninfo!("message");\nlet value = 42;\ninfo!("value is'
        '{}", value);\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[tracing_prefix]:" not in result.output


def test_run_tracing_prefix_clean_all_imports(tmp_path: Path) -> None:
    """Test run passes with all tracing imports."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "use tracing::{debug, error, info, instrument, trace, warn};\n"
        "\n"
        "fn foo() {\n"
        '    info!("info");\n'
        '    error!("error");\n'
        '    warn!("warn");\n'
        '    debug!("debug");\n'
        '    trace!("trace");\n'
        "}\n"
        "\n"
        "#[instrument]\n"
        "fn bar() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[tracing_prefix]:" not in result.output
