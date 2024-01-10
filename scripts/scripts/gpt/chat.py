import typer
from scripts.gpt.lib import run_noninteractive

app = typer.Typer()


@app.command()
def chat(prompt: str, model: str = "gpt-4-1106-preview"):
    run_noninteractive(prompt, model=model)


if __name__ == "__main__":
    app()
