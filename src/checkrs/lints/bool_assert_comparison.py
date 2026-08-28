"""Lint: bool comparison in assert macros."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


_MIN_TOKEN_TREE_CHILDREN = 2
_MIN_ASSERT_ARGS = 2


def _extract_args(token_tree: ast_grep_py.SgNode) -> list[str]:
    """Extract top-level comma-separated arguments from a token_tree."""
    children = list(token_tree.children())
    if len(children) < _MIN_TOKEN_TREE_CHILDREN:
        return []
    inner = children[1:-1]  # strip '(' and ')'
    args: list[str] = []
    cur: list[ast_grep_py.SgNode] = []
    for child in inner:
        if child.text() == ",":
            args.append("".join(n.text() for n in cur).strip())
            cur = []
        else:
            cur.append(child)
    if cur:
        args.append("".join(n.text() for n in cur).strip())
    return args


def _is_bool_literal(value: str) -> bool:
    """Return True if value is a boolean literal."""
    return value in ("true", "false")


class BoolAssertComparison(Lint):
    """bool comparison in assert macros."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "bool_assert_comparison"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "assert with boolean comparison"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `assert_eq!` and `assert_ne!` (and their `debug_`"
            " variants) where one of the compared values is a boolean literal"
            " `true` or `false`, which is redundant and less clear than using"
            " `assert!` directly."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Using `assert_eq!` to compare a value with `true` or `false` is"
            " verbose and obscures intent. `assert!(cond)` and `assert!(!cond)`"
            " are clearer and give better failure messages.\n"
            "\n"
            "Bad:\n"
            "```rust\n"
            "assert_eq!(x > 0, true);\n"
            "assert_eq!(x, false);\n"
            "assert_eq!(true, y);\n"
            "```\n"
            "\n"
            "Good:\n"
            "```rust\n"
            "assert!(x > 0);\n"
            "assert!(!x);\n"
            "assert!(y);\n"
            "```\n"
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
            "// Bad\n"
            "assert_eq!(x > 0, true);\n"
            "assert_eq!(x, false);\n"
            "assert_ne!(x, true);\n"
            "debug_assert_eq!(y, true);\n"
            "\n"
            "// Good\n"
            "assert!(x > 0);\n"
            "assert!(!x);\n"
            "assert!(!x);\n"
            "debug_assert!(y);\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use `assert!(...)` instead of `assert_eq!` with `true`/`false`"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {"pattern": "assert_eq!($$$ARGS)"},
                    {"pattern": "assert_ne!($$$ARGS)"},
                    {"pattern": "debug_assert_eq!($$$ARGS)"},
                    {"pattern": "debug_assert_ne!($$$ARGS)"},
                ]
            },
        )
        violations: list[Violation] = []
        for m in node.find_all(config):
            token_tree = next(
                (c for c in m.children() if c.kind() == "token_tree"), None
            )
            if token_tree is None:
                continue
            args = _extract_args(token_tree)
            if len(args) < _MIN_ASSERT_ARGS:
                continue
            if _is_bool_literal(args[0]) or _is_bool_literal(args[1]):
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
