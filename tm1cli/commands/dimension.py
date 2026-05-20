from typing import Annotated, Optional

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.list_utils import OutputFormat, apply_filter, apply_paging, render_output
from tm1cli.utils.various import resolve_database
from tm1cli.utils.watch import watch_option

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command(name="list")
def list_dimension(
    ctx: typer.Context,
    database: Annotated[str, DATABASE_OPTION] = None,
    skip_control_dims: Annotated[
        bool,
        typer.Option(
            "-s",
            "--skip-control-dims",
            help="Exclude control dimensions (names starting with '}').",
        ),
    ] = False,
    filter: Annotated[Optional[str], typer.Option("--filter", "-f", help="Regex/substring filter (case-insensitive).")] = None,
    output: Annotated[OutputFormat, typer.Option("--output", "-o", help="Output format: yaml (default) or json.")] = "yaml",
    limit: Annotated[Optional[int], typer.Option("--limit", help="Maximum number of results to return.")] = None,
    offset: Annotated[int, typer.Option("--offset", help="Number of results to skip (for paging).", min=0)] = 0,
):
    """
    List dimensions
    """
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        names = tm1.dimensions.get_all_names(skip_control_dims=skip_control_dims)
    names = apply_filter(names, filter)
    result = apply_paging(names, limit, offset)
    typer.echo(render_output(result, output))


@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    dimension_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """
    Check if dimension exists
    """
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.dimensions.exists(dimension_name))
