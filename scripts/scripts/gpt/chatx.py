import typer
from scripts.gpt.lib import run_propose

app = typer.Typer()


@app.command()
def chatx(prompt: str, model: str = "gpt-4-1106-preview"):
    run_propose(prompt, model=model)


if __name__ == "__main__":
    app()
