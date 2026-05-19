"""Lint: must_use attributes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class MustUseAttribute(Lint):
    """must_use attributes."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "must_use_attribute"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "must_use attributes"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "The #[must_use] attribute can lead to code bloat and excessive"
            "compiler warnings. Function return value usage should be handled by"
            "caller's logic, not enforced by compiler. Consider removing the"
            "attribute to simplify the code."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "The #[must_use] attribute can lead to code bloat and excessive"
            "compiler warnings. Function return value usage should be handled by"
            "caller's logic, not enforced by compiler. Consider removing the"
            "attribute to simplify the code."
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
        return "remove must_use attributes"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "attribute"},
                    {"has": {"kind": "identifier", "regex": "^must_use$"}},
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
