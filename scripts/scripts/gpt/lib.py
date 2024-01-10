# Ask for a completion from the OpenAI API using gpt-4

import os
import subprocess

from openai import OpenAI
import typer
from rich.console import Console

console = Console()
print = console.print

app = typer.Typer()

SYSTEM_PROMPT = (
    "\n\n"
    "Please generate the shortest answer you can that is informative. "
    "This will be displayed directly in the terminal. The ideal output "
    "is one line of code and one line describing what the command does. "
    "Less than 5 is still good. Remember, this will be displayed directly "
    "in the terminal, so do not include markdown formatting and code to be "
    "run directly should on its own line. It's really important that we don't"
    "have markdown codeblocks that use backticks (` or ```)."
)
SYSTEM_PROMPT_PROPOSE = (
    "\n\n"
    "Please generate a one-line bash command as well as one or more comment lines. This will be presented to the user"
    "as a suggestion and then automatically executed. It's really important that we don't"
    "have markdown codeblocks that use backticks (` or ```). If you want to include a comment,"
    "please use a #. It is absolutely essential that the command is one line and that anything"
    "that is not code is a comment."
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def complete(
    prompt: str, model: str, conversation: list[str], write_output: bool = True
):
    messages = []
    for i, text in enumerate(conversation):
        if i % 2 == 0:
            messages.append({"role": "user", "content": text})
        else:
            messages.append({"role": "assistant", "content": text})

    messages.append({"role": "user", "content": prompt})
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


def run_interactive(
    model: str = "gpt-4-1106-preview", system_prompt: str = SYSTEM_PROMPT
):
    conversation = []
    try:
        print(f"[blue]Now chatting with {model}. Press Ctrl-C to exit.")
        while True:
            prompt = typer.prompt("Prompt")
            conversation.append(prompt)

            final = prompt + system_prompt
            print(prompt, style="white")
            response = complete(final, model=model, conversation=conversation)
            conversation.append(response)
    except typer.Abort:
        print()
        print("[red bold]User aborted.")
    except KeyboardInterrupt:
        print("Chat done")


def run_noninteractive(
    prompt: str, model: str = "gpt-4-1106-preview", system_prompt: str = SYSTEM_PROMPT
):
    conversation = [prompt]
    final = prompt + system_prompt
    complete(final, model=model, conversation=conversation)


def run_propose(
    prompt: str,
    model: str = "gpt-4-1106-preview",
    system_prompt: str = SYSTEM_PROMPT_PROPOSE,
    auto_exec: bool = False,
):
    try:
        conversation = [prompt]
        final = prompt + system_prompt
        response = complete(final, model=model, conversation=conversation)
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
