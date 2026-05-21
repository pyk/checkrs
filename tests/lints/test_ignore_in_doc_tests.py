"""Tests for the ``ignore_in_doc_tests`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_ignore_in_doc_tests(tmp_path: Path) -> None:
    """Test run detects ignore_in_doc_tests violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "/// ```ignore\n/// use oscar::providers::zai::{ChatCompletionRequestBuilder,"
        "MessageRole};\n///\n/// let request ="
        'ChatCompletionRequestBuilder::new("glm-4.7")\n///    '
        '.message(MessageRole::System, "You are a helpful assistant.")\n///    '
        '.message(MessageRole::User, "Hello!")\n///     .temperature(0.7)\n///    '
        ".build()?;\n/// ```\npub fn example() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "ignore_in_doc_tests" in result.output
    assert "help: use no_run instead of ignore in doc tests" in result.output


def test_run_ignore_in_doc_tests_rust_ignore(tmp_path: Path) -> None:
    """Test run detects `rust,ignore` doc test violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        '//! ```rust,ignore\n'
        '//! let config = Config::new()\n'
        '//!     .urls(vec!["https://mainnet.example.com".into()])\n'
        '//!     .block(18_000_000)\n'
        '//!     .chain_id(1);\n'
        '//!\n'
        '//! config.validate()?;\n'
        '//! ```\n'
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "error[ignore_in_doc_tests]:" in result.output
    assert "help: use no_run instead of ignore in doc tests" in result.output


def test_run_ignore_in_doc_tests_clean(tmp_path: Path) -> None:
    """Test run passes when no ignore_in_doc_tests violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "/// ```no_run\n/// use oscar::providers::zai::{ChatCompletionRequestBuilder,"
        "MessageRole};\n///\n/// let request ="
        'ChatCompletionRequestBuilder::new("glm-4.7")\n///    '
        '.message(MessageRole::System, "You are a helpful assistant.")\n///    '
        ".build()?;\n/// ```\npub fn example() {}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[ignore_in_doc_tests]:" not in result.output
