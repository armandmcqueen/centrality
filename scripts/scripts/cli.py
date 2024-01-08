import typer
from rich.console import Console

console = Console()

app = typer.Typer()


@app.command()
def main():
    console.log("Hello world!")


if __name__ == "__main__":
    app()
