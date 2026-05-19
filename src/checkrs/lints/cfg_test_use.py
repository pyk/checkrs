"""Lint: using #[cfg(test)] outside mod tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CfgTestUse(Lint):
    """using #[cfg(test)] outside mod tests."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "cfg_test_use"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "using #[cfg(test)] outside mod tests"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Checks that `#[cfg(test)]` only annotates `mod tests` items."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Test-only code should live inside a single `mod tests` block rather "
            "than scattering `#[cfg(test)]` on individual imports or functions. "
            "This keeps the module structure predictable and easier to follow."
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
            "#[cfg(test)]\n"
            "mod tests {\n"
            "    //\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "place #[cfg(test)] only before mod tests"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "attribute_item",
                "pattern": "#[cfg(test)]",
            },
        )
        matches = list(node.find_all(config))

        violations: list[Violation] = []
        for m in matches:
            n = m.next()
            while n is not None and n.kind() in (
                "attribute_item",
                "line_comment",
                "block_comment",
            ):
                n = n.next()

            if n is not None and n.kind() == "mod_item":
                name_node = n.field("name")
                if name_node is not None and name_node.text() == "tests":
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
