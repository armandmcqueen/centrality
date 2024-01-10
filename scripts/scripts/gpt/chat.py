import typer
from scripts.gpt.lib import run_noninteractive
from typing import Optional
from scripts.gpt.persistence import Chat

app = typer.Typer()


@app.command()
def chat(
    prompt: str, model: str = "gpt-4-1106-preview", clear_history: Optional[bool] = None
):
    if clear_history:
        Chat().clear_history()
        return
    run_noninteractive(prompt, model=model)


if __name__ == "__main__":
    app()
