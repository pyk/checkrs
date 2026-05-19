"""Lint: std::process::Command fully-qualified paths."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class StdProcessPrefix(Lint):
    """std::process::Command fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "std_process_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return (
            "use a 'use std::process::Command;' statement instead of the fully"
            "qualified path"
        )

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Prefer importing `std::process::Command` at the top of the file and"
            "using `Command::function()` directly."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            'Bad: let mut cmd = std::process::Command::new("cargo");'
            'cmd.args(["doc", "--package", crate_name]); let child:'
            "std::process::Child = cmd.spawn().unwrap();"
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n// No example provided\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "import Command instead of using the fully qualified path"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {"pattern": "std::process::Command::$METHOD($$$ARGS)"},
                    {
                        "all": [
                            {"kind": "scoped_type_identifier"},
                            {"regex": "std::process::Command"},
                        ]
                    },
                ]
            },
        )
        matches = list(node.find_all(config))

        return [
            Violation(
                lint_name=self.name,
                file_path=file_path,
                line=m.range().start.line + 1,
                column=m.range().start.column + 1,
                message="found",
            )
            for m in matches
        ]
