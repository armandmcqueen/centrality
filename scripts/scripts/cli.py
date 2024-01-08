import typer
from rich.console import Console
from scripts.sync_with_remote import watch_and_sync
from scripts.upgrade_dep import upgrade as run_upgrade

console = Console()

app = typer.Typer()


@app.command(
    help="Say hello!",
)
def hello_world():
    console.log("Hello world!")


@app.command(
    help="Watch a local directory and sync it to the remote destination whenever it changes.",
)
def sync(
    local_directory: str = typer.Argument(
        ...,
        help="The local directory to watch and sync, e.g. ../vmagent",
    ),
    host: str = typer.Argument(
        ...,
        help="The remote host to sync to, e.g. ubuntu@1.1.1.1",
    ),
):
    watch_and_sync(local_directory, host)


@app.command(
    help="Upgrade a dependency in all pyproject.toml files in the monorepo",
)
def upgrade(
    dependency_name: str = typer.Argument(
        ...,
        help="The name of the dependency to upgrade, e.g. rich",
    ),
    old_version: str = typer.Argument(
        ...,
        help="The old version of the dependency to upgrade, e.g. 10.2.2",
    ),
    new_version: str = typer.Argument(
        ...,
        help="The new version of the dependency to upgrade, e.g. 10.3.0",
    ),
):
    run_upgrade(dependency_name, old_version, new_version)


if __name__ == "__main__":
    app()
