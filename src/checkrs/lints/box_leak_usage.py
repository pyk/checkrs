"""Lint: Box::leak usage."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class BoxLeakUsage(Lint):
    """Box::leak usage."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "box_leak_usage"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "Box::leak usage"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Box::leak creates a 'static lifetime for data that will never be"
            "deallocated. This is generally a bad practice except in very"
            "specific cases like: - Singleton patterns with truly global lifetime"
            "- FFI with C code that manages the memory - Performance-critical"
            "code where allocation overhead is unacceptable"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Prefer using proper lifetime management or Arc<RwLock<T>> for sharedstate."
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
        return "avoid intentional memory leaks with Box::leak"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={"pattern": "Box::leak($$ARG)"},
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
