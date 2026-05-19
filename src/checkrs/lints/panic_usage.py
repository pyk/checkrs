"""Lint: panic! usage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class PanicUsage(Lint):
    """panic! usage."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "panic_usage"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "panic! usage"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Functions that use `panic!` are fallible and should return a"
            "`Result` type to allow proper error handling by callers. The"
            "`panic!` macro causes the entire program to abort, which is"
            "inappropriate for recoverable errors."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```rust let style = match"
            'ProgressStyle::default_spinner() .tick_strings(&["⠋", "⠙", "⠹", "⠸",'
            '"⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]) .template("{spinner} {msg}") {'
            'Ok(style) => style, Err(e) => panic!("Failed to create spinner'
            'template: {}", e), }; ```'
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
            "let style = match ProgressStyle::default_spinner()\n"
            '    .tick_strings(&["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])\n'
            '    .template("{spinner} {msg}")\n'
            "{\n"
            "    Ok(style) => style,\n"
            '    Err(e) => panic!("Failed to create spinner template: {}", e),\n'
            "};\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "return Result instead of panicking"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "pattern": "panic!($$$ARGS)",
                "not": {
                    "any": [
                        {"inside": {"pattern": "mod tests { $$$ }", "stopBy": "end"}}
                    ]
                },
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
