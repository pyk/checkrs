"""Lint: parking_lot::RwLock fully-qualified paths."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class ParkingLotRwlock(Lint):
    """parking_lot::RwLock fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "parking_lot_rwlock"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "parking_lot::RwLock used with fully qualified path"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `parking_lot::RwLock` written as a fully qualified"
            "path instead of being imported and used as `RwLock`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Importing `parking_lot::RwLock` keeps code concise"
            "and consistent with project conventions."
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
            "let lock = parking_lot::RwLock::new(42);\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import RwLock and use it without the parking_lot:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {
                        "all": [
                            {"kind": "scoped_type_identifier"},
                            {"regex": "parking_lot::RwLock\\b"},
                        ]
                    },
                    {
                        "pattern": "parking_lot::RwLock::$METHOD($$$ARGS)"},
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
