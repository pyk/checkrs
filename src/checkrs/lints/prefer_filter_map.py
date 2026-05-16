"""Lint: filter_map() not used in map().filter().map() chains."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class PreferFilterMap(Lint):
    """filter_map() not used in map().filter().map() chains."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "prefer_filter_map"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "filter_map() not used in map().filter().map() chains"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "The combination of `map().filter().map()` can be simplified to a"
            "single `filter_map` call, which is more concise and idiomatic. For"
            "example, `.map(|s| s.parse()).filter(|s| s.is_ok()).map(|s|"
            "s.unwrap())` can be rewritten as `.filter_map(|s| s.parse().ok())`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "The combination of `map().filter().map()` can be simplified to a"
            "single `filter_map` call, which is more concise and idiomatic. For"
            "example, `.map(|s| s.parse()).filter(|s| s.is_ok()).map(|s|"
            "s.unwrap())` can be rewritten as `.filter_map(|s| s.parse().ok())`."
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
        return "use filter_map instead of map().filter().map()"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "pattern": "$ITER.map(|$A| $MAP_EXPR).filter(|$B|"
                "$FILTER_EXPR).map(|$C| "
                "$MAP2_EXPR)"
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
