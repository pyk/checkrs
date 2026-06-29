"""Lint: pub(crate) visibility modifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class PubCrateVisibility(Lint):
    """pub(crate) visibility modifier."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "pub_crate_visibility"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "pub(crate) visibility modifier"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Detects `pub(crate)` visibility modifiers and suggests using"
            " `pub` instead."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "`pub(crate)` is more restrictive than `pub` and is often used when"
            " `pub` would suffice. In many codebases, items that need to be"
            " visible within the crate can simply be `pub`."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "This lint does not check whether the item is actually used across"
            " crate boundaries. Manually verify that changing to `pub` does not"
            " unintentionally widen the API surface."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "// Violation\n"
            "pub(crate) struct IssueCount {\n"
            "    pub(crate) severity: String,\n"
            "}\n"
            "\n"
            "// Clean\n"
            "pub struct IssueCount {\n"
            "    pub severity: String,\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use `pub` instead of `pub(crate)`"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "visibility_modifier",
                "has": {
                    "kind": "crate",
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
