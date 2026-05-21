"""Lint: use `std::fs` module import instead of fully-qualified `std::fs::` calls."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class StdFsPrefix(Lint):
    """use `std::fs` module import instead of fully-qualified `std::fs::` calls."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "std_fs_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "fully-qualified `std::fs::` call instead of `fs::` module import"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for calls like `std::fs::read(...)` and requires importing "
            "the module with `use std::fs;` so the call becomes `fs::read(...)`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Fully-qualified `std::fs::` paths are verbose. "
            "Import the `std::fs` module and use the `fs::` prefix instead.\n"
            "\n"
            "Bad:\n"
            "```rust\n"
            "std::fs::read_to_string(&path)?;\n"
            "std::fs::write(&path, &content)?;\n"
            "```\n"
            "\n"
            "Good:\n"
            "```rust\n"
            "use std::fs;\n"
            "\n"
            "fs::read_to_string(&path)?;\n"
            "fs::write(&path, &content)?;\n"
            "```\n"
            "\n"
            "Do not import individual items like `use std::fs::read;` "
            "or `use std::fs::{read, write};`."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "// Bad\n"
            "std::fs::read_to_string(&path)?;\n"
            "\n"
            "// Good\n"
            "use std::fs;\n"
            "fs::read_to_string(&path)?;\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import `std::fs` and call functions via `fs::function_name()`"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"all": [{"pattern": "std::fs::$METHOD($$$ARGS)"}]},
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
