"""Lint: comment banner."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CommentBanner(Lint):
    """comment banner."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "comment_banner"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "comment banner"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Flags banner-style line comments like `// ---- Foo ----`."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Banner comments add noise without explaining the code. Prefer a"
            " comment that describes the nearby logic directly."
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
            "// ---- Foo ----\n"
            "pub fn extract_id(input: &str) -> Option<u64> {\n"
            "    // ...\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "remove banner-style divider comments"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"regex": r"^// ---- .+ ----$"},
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
