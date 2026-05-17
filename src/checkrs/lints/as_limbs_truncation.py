"""Lint: as_limbs()[0] silently truncates multi-limb integers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class AsLimbsTruncation(Lint):
    """Checks for .as_limbs()[0] which discards higher-order limbs."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "as_limbs_truncation"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "as_limbs()[0] truncates big integers"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Detects `.as_limbs()[0]` on big integer types. "
            "This pattern reads only the lowest u64 limb and silently discards "
            "higher limbs, truncating values larger than `u64::MAX`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Multi-limb integers (e.g., U256) spread their value across multiple "
            "`u64` limbs. Indexing only the first limb is almost always a bug when "
            "the intent is to convert the entire value to `u64`, because it wraps "
            "or truncates instead of saturating or failing explicitly."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "May flag legitimate uses where the caller has already verified the "
            "value fits in a single limb. In those cases, prefer an explicit cast "
            "or a clarifying comment."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "// Bad: silently truncates values > u64::MAX\n"
            "let ts = new_state.cheatcodes.warp_timestamp;\n"
            "new_state.block_timestamp = ts.as_limbs()[0];\n"
            "\n"
            "// Good: saturates at u64::MAX\n"
            "new_state.block_timestamp = u64::try_from(ts).unwrap_or(u64::MAX);\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return (
            "use `u64::try_from(val).unwrap_or(u64::MAX)` or another explicit "
            "saturating conversion instead of `.as_limbs()[0]`"
        )

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "pattern": "$EXPR.as_limbs()[0]",
            },
        )
        matches = list(node.find_all(config))

        return [
            Violation(
                lint_name=self.name,
                file_path=file_path,
                line=m.range().start.line + 1,
                column=m.range().start.column + 1,
                message="truncates",
            )
            for m in matches
        ]
