import typer
from scripts.gpt.lib import run_interactive

app = typer.Typer()


@app.command()
def chat(model: str = "gpt-4-1106-preview"):
    run_interactive(model=model)


if __name__ == "__main__":
    app()
