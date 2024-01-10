import typer
from scripts.gpt.lib import run_interactive
from scripts.gpt.persistence import Chat
from typing import Optional

app = typer.Typer()


@app.command()
def chati(model: str = "gpt-4-1106-preview", clear_history: Optional[bool] = None):
    if clear_history:
        Chat().clear_history()
        return
    run_interactive(model=model)


if __name__ == "__main__":
    app()
