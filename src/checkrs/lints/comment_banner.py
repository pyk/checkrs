"""Lint: comment banner."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py

_BANNER_DASHES = "-" * 50

_DASH_LINE = re.compile(r"^// -+$")


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
        return (
            "Flags single-line banner comments like `// ---- Foo ----` and"
            " three-line banner dividers like `// ---\\n// text\\n// ---`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Banner comments add visual noise without explaining the code."
            " Prefer a comment that describes the nearby logic directly, or"
            " split code with blank lines instead of decorative dividers."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        d = _BANNER_DASHES
        return f"```rust\n// {d}\n// Tests\n// {d}\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "remove unnecessary banner/section separator comments"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        single_config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"regex": r"^// ---- .+ ----$"},
                ]
            },
        )
        dash_line_config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"regex": r"^// -+$"},
                ]
            },
        )

        violations: list[Violation] = []

        for m in node.find_all(single_config):
            r = m.range()
            violations.append(
                Violation(
                    lint_name=self.name,
                    file_path=file_path,
                    line=r.start.line + 1,
                    column=r.start.column + 1,
                    message="found",
                ),
            )

        for m in node.find_all(dash_line_config):
            text_node = m.next()
            if text_node is None or text_node.kind() != "line_comment":
                continue
            bottom_node = text_node.next()
            if bottom_node is None or bottom_node.kind() != "line_comment":
                continue
            text = text_node.text()
            bottom = bottom_node.text()
            if _DASH_LINE.match(text) or not _DASH_LINE.match(bottom):
                continue

            r = m.range()
            violations.append(
                Violation(
                    lint_name=self.name,
                    file_path=file_path,
                    line=r.start.line + 1,
                    column=r.start.column + 1,
                    message="found",
                ),
            )

        return violations
