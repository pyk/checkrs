"""Lint: unsafe usage."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class UnsafeUsage(Lint):
    """unsafe usage."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "unsafe_usage"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "unsafe usage"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Detects all forms of `unsafe` usage in Rust code, including "
            "`unsafe` blocks, `unsafe fn` functions, `unsafe impl` trait "
            "implementations, and `unsafe trait` trait definitions."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Unsafe code bypasses Rust's memory safety guarantees and can "
            "lead to undefined behavior, memory corruption, and security "
            "vulnerabilities. Prefer safe alternatives and encapsulate any "
            "required unsafe operations behind safe abstractions."
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
            "unsafe {\n"
            "    std::ptr::write_bytes(map_ptr, 0, crate::inspector::MAP_SIZE)\n"
            "};\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "avoid unsafe code"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "unsafe { $$$ }"},
                    {"pattern": "unsafe fn $$$"},
                    {"pattern": "unsafe impl $$$"},
                    {"pattern": "unsafe trait $$$"},
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
