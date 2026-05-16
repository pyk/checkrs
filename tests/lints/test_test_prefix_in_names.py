"""Tests for the ``test_prefix_in_names`` lint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from checkrs.main import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_run_test_prefix_in_names(tmp_path: Path) -> None:
    """Test run detects test_prefix_in_names violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "#[test]\nfn test_builder_minimal_fields() {\n    let request ="
        'ChatCompletionRequestBuilder::new("glm-4.7")\n       '
        '.message(MessageRole::System, "You are helpful.")\n       '
        '.message(MessageRole::User, "Hello!")\n        .build()\n       '
        '.unwrap();\n\n    assert_eq!(request.model, "glm-4.7");\n   '
        "assert_eq!(request.messages.len(), 2);\n    assert_eq!(request.stream,"
        "None);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert result.exit_code == 1
    assert "test_prefix_in_names" in result.output
    assert "help: remove test_ prefix from test function names" in result.output


def test_run_test_prefix_in_names_clean(tmp_path: Path) -> None:
    """Test run passes when no test_prefix_in_names violations."""
    rust_file = tmp_path / "main.rs"
    rust_file.write_text(
        "//! Clean test module.\n"
        "\n"
        "#[test]\nfn builder_minimal_fields() {\n    assert!(true);\n}\n"
    )
    result = runner.invoke(app, ["run", str(rust_file)])
    assert "error[test_prefix_in_names]:" not in result.output
