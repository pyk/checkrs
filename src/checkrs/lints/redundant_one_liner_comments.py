"""Lint: redundant one-liner comments."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class RedundantOneLinerComments(Lint):
    """redundant one-liner comments."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "redundant_one_liner_comments"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "redundant one-liner comments"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Remove obvious comments that restate what the code does. Comments"
            'should explain "why" something is done, not "what" is being done.'
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Good: No comment at all (code is self-explanatory) Bad: `// Get"
            "cargo metadata` followed by `cargo::metadata()?`"
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
        return "remove comments that merely restate the code"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"not": {"has": {"kind": "outer_doc_comment_marker"}}},
                    {"not": {"has": {"kind": "inner_doc_comment_marker"}}},
                    {
                        "not": {
                            "regex": (
                                "^\\s*//\\s*(TODO|FIXME|NOTE|HACK|WARNING|FIX)\\s*:"
                            ),
                        }
                    },
                    {"not": {"precedes": {"kind": "line_comment"}}},
                    {"not": {"follows": {"kind": "line_comment"}}},
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
