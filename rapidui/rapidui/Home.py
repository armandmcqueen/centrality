from rapidui.header import header
from rapidui.library.utils import load_config
import typer


cli = typer.Typer()


@cli.command()
def app():
    _ = load_config()
    header("Home")


if __name__ == "__main__":
    cli(standalone_mode=False)
