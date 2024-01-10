import typer
from scripts.gpt.lib import run_propose
from typing import Optional
from scripts.gpt.persistence import Chat

app = typer.Typer()


@app.command()
def chatx(
    prompt: str, model: str = "gpt-4-1106-preview", clear_history: Optional[bool] = None
):
    if clear_history:
        Chat().clear_history()
        return
    run_propose(prompt, model=model)


if __name__ == "__main__":
    app()
