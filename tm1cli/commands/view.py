from typing import Annotated, Optional

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.list_utils import OutputFormat, VisibilityType, apply_filter, apply_paging, render_output
from tm1cli.utils.various import resolve_database
from tm1cli.utils.watch import watch_option

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command(name="list")
def list_view(
    ctx: typer.Context,
    cube: Annotated[Optional[str], typer.Option("--cube", "-c", help="Scope to a specific cube name.")] = None,
    type: Annotated[
        VisibilityType,
        typer.Option("--type", "-t", help="Visibility filter: public, private, or both."),
    ] = "public",
    database: Annotated[str, DATABASE_OPTION] = None,
    filter: Annotated[Optional[str], typer.Option("--filter", "-f", help="Regex/substring filter (case-insensitive).")] = None,
    output: Annotated[OutputFormat, typer.Option("--output", "-o", help="Output format: yaml (default) or json.")] = "yaml",
    limit: Annotated[Optional[int], typer.Option("--limit", help="Maximum number of results to return.")] = None,
    offset: Annotated[int, typer.Option("--offset", help="Number of results to skip (for paging).", min=0)] = 0,
):
    """
    List views
    """
    include_public = type in ("public", "both")
    include_private = type in ("private", "both")
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        cube_names = [cube] if cube else tm1.cubes.get_all_names(skip_control_cubes=True)
        results: list[dict] = []
        for cube_name in cube_names:
            private_names, public_names = tm1.views.get_all_names(cube_name)
            if include_public:
                for name in public_names:
                    results.append({"cube": cube_name, "name": name, "type": "public"})
            if include_private:
                for name in private_names:
                    results.append({"cube": cube_name, "name": name, "type": "private"})
    if filter:
        matching = set(apply_filter([r["name"] for r in results], filter))
        results = [r for r in results if r["name"] in matching]
    typer.echo(render_output(apply_paging(results, limit, offset), output))


@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    cube_name: str,
    view_name: str,
    is_private: Annotated[
        bool, typer.Option("-p", "--private", help="Flag to specify if view is private")
    ] = False,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """
    Check if view exists
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.views.exists(cube_name, view_name, is_private))
