# Ask for a completion from the OpenAI API using gpt-4

import os
import subprocess

import subprocess
import typer
from scripts.gpt.persistence import UserTurn, AssistantTurn, ChatEntry, Chat
from openai import OpenAI
import os
from rich.console import Console
import typer
from rich.console import Console
from scripts.gpt.persistence import (
    UserTurn,
    AssistantTurn,
    ChatEntry,
    Chat,
)

console = Console()
print = console.print

app = typer.Typer()


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def complete(
    prompt: str, model: str, conversation: list[ChatEntry], write_output: bool = True
):
    messages = []
    for entry in conversation:
        messages.append(entry.as_json())

    messages.append(UserTurn(prompt).as_json())
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    if write_output:
        print()
    out = ""
    for chunk in stream:
        out_chunk = chunk.choices[0].delta.content or ""
        out += out_chunk
        if write_output:
            print(out_chunk, end="", style="deep_sky_blue2")

    if write_output:
        print()
        print()

    return out


def run_interactive(model: str = "gpt-4-1106-preview"):
    chat = Chat()
    try:
        print(f"[blue]Now chatting with {model}. Press Ctrl-C to exit.")
        if len(chat.history) > 0:
            print(
                f"[white]{len(chat.history)} turns in history. `chats clear` to clear | `chats disable` to disable"
            )
        while True:
            prompt = typer.prompt("Chat")
            final = prompt + "\n\n" + chat.config.chat_system_prompt
            print(prompt, style="white")
            chat.add_entry(UserTurn(prompt))
            response = complete_chat_stream(final, model=model, conversation=chat.history[:-1])
            chat.add_entry(AssistantTurn(response))
    except typer.Abort:
        print()
        print("[red bold]User aborted.")
    except KeyboardInterrupt:
        print("Chat done")


def run_noninteractive(prompt: str, model: str = "gpt-4-1106-preview"):
    chat = Chat()
    chat.add_entry(UserTurn(prompt))
    final = prompt + "\n\n" + chat.config.chat_system_prompt
    response = complete_chat_stream(final, model=model, conversation=chat.history[:-1])
    chat.add_entry(AssistantTurn(response))


def run_propose(
    prompt: str,
    model: str = "gpt-4-1106-preview",
    auto_exec: bool = False,
):
    try:
        chat = Chat()
        chat.add_entry(UserTurn(prompt))
        final = prompt + "\n\n" + chat.config.chatx_system_prompt
        response = complete_chat_stream(final, model=model, conversation=chat.history[:-1])
        chat.add_entry(AssistantTurn(response))
        if not auto_exec:
            inp = typer.prompt("[exec? Y/n]", default="Y", show_default=False)
            if inp.strip().lower() not in ["y", ""]:
                print("Aborting")
                return
        for line in response.splitlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            subprocess.check_call(line, shell=True, stderr=subprocess.STDOUT)
    except typer.Abort:
        print()
        print("[red bold]User aborted.")
