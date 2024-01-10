import typer
from scripts.gpt.persistence import Chat
from pathlib import Path
from rich import print

app = typer.Typer()


@app.command(
    help="Disable history. To re-enable, use `enable`. This is different "
    "from clearing history, which can be done with `clear`"
)
def disable():
    chat = Chat()
    chat.disable_history()
    print("[bright_black]History disabled")


@app.command(help="Enable history. This is the default.")
def enable():
    chat = Chat()
    chat.enable_history()
    print("[green]History enabled")


@app.command(help="Clear history. To disable history, use `disable`.")
def clear():
    chat = Chat()
    chat.clear_history()
    print("[deep_sky_blue4]History cleared")


@app.command(help="View history.")
def show():
    chat = Chat()
    for turn in chat.history:
        print(turn)


@app.command(help="View raw history. For debugging.")
def raw():
    chat = Chat()
    print(chat.history_file_contents)


@app.command(help="View settings")
def config():
    chat = Chat()
    chat.display_config()


@app.command(help="Set chatx system prompt")
def set_chatx_prompt(prompt: str):
    if Path(prompt).exists():
        print(f"Reading from file {Path(prompt).absolute()}")
        prompt = Path(prompt).read_text()
    chat = Chat()
    chat.set_chatx_system_prompt(prompt)
    chat.display_config()


@app.command(help="Set chat system prompt")
def set_chat_prompt(prompt: str):
    if Path(prompt).exists():
        print(f"Reading from file {Path(prompt).absolute()}")
        prompt = Path(prompt).read_text()
    chat = Chat()
    chat.set_chat_system_prompt(prompt)
    chat.display_config()


@app.command(help="Reset config")
def reset():
    chat = Chat()
    chat.clear_history()
    chat.config_file.unlink()


if __name__ == "__main__":
    app()
