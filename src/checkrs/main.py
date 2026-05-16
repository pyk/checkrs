"""Entrypoint for the checkrs CLI."""

from __future__ import annotations

import pathlib
import sys
from importlib.metadata import version

import typer

from checkrs.commands.rules import list_lints
from checkrs.commands.run import run as run_command

app = typer.Typer(name="checkrs", no_args_is_help=True)


def _version_callback(*, value: bool) -> None:
    if value:
        sys.stdout.write(f"checkrs {version('checkrs')}\n")
        raise typer.Exit


_OPTION_DEFAULT = False

_VERSION_OPTION = typer.Option(
    _OPTION_DEFAULT,
    "--version",
    callback=_version_callback,
    is_eager=True,
    help="Show version and exit.",
)

_PATH_ARG = typer.Argument(
    ...,
    exists=True,
    help="Path to a Rust file or directory.",
)


@app.callback()
def main(
    *,
    version: bool = _VERSION_OPTION,
) -> None:
    """Checkrs - A Rust linter."""


@app.command()
def run(
    path: pathlib.Path = _PATH_ARG,
) -> None:
    """Run the linter."""
    p = pathlib.Path(path)
    exit_code = run_command(p)
    raise typer.Exit(exit_code)


@app.command(name="lints")
def lints_cmd() -> None:
    """Show list of linters."""
    list_lints()
