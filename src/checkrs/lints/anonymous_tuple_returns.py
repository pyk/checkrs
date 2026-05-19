"""Lint: anonymous tuple returns with 3+ elements."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnonymousTupleReturns(Lint):
    """anonymous tuple returns with 3+ elements."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anonymous_tuple_returns"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "anonymous tuple returns with 3+ elements"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Anonymous tuples with 3+ elements are hard to understand and"
            "maintain. Consider using a named struct instead."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "# Before ```rust fn generate_method_params_and_call( inputs:"
            "&syn::punctuated::Punctuated<syn::FnArg, syn::Token![,]>, ) ->"
            "syn::Result<( Vec<syn::Ident>, Vec<syn::Type>,"
            "Vec<proc_macro2::TokenStream>, )> { // ... } ```"
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
            "fn generate_method_params_and_call(\n"
            "    inputs: &syn::punctuated::Punctuated<syn::FnArg, syn::Token![,]>,\n"
            ") -> syn::Result<(\n"
            "    Vec<syn::Ident>,\n"
            "    Vec<syn::Type>,\n"
            "    Vec<proc_macro2::TokenStream>,\n"
            ")> {\n"
            "    // ...\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use a named struct for tuple returns with 3+ elements"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "tuple_type",
                "any": [
                    {"has": {"kind": "generic_type", "nthChild": 3}},
                    {"has": {"kind": "primitive_type", "nthChild": 3}},
                    {
                        "has": {"kind": "type_identifier", "nthChild": 3},
                        "inside": {"kind": "function_item"},
                    },
                ],
                "inside": {
                    "any": [{"kind": "function_item"}, {"kind": "type_arguments"}]
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
