# Utility to help pass config to streamlit via envvar. This is a workaround for lack of argument support
# in multi-page apps (if you want people to be able to go directly to a page via a URL instead of going
# through the home page).

from rapidui.library.config import StreamlitUiConfig
from pathlib import Path
from typing import Annotated, Optional
import typer


cli = typer.Typer()


@cli.command(name="set")
def set_var(
    file: Annotated[Optional[str], typer.Option("--file", "-f")] = None,
):
    """Print out the correct export command to set the envvar. This should then be exec'd verbatim"""

    if file:
        config = StreamlitUiConfig.from_yaml_file(Path(file))
    else:
        config = StreamlitUiConfig()
    print(f"export {config.envvar_name()}={config.to_dict_str()}")


@cli.command()
def unset():
    """Print out the correct export command to unset the envvar. This should then be exec'd verbatim"""
    print(f"unset {StreamlitUiConfig.envvar_name()}")


if __name__ == "__main__":
    cli()
