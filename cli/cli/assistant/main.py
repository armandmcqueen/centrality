from scripts.gpt.lib import complete
from scripts.gpt.persistence import (
    SystemTurn,
)
from pathlib import Path
from cli.assistant.sandbox import run_code, write_tmp_and_entrypoint_files
from rich import print
import typer


system_prompt_file = Path(__file__).parent / "SYSTEM_PROMPT.txt"
system_prompt = system_prompt_file.read_text()

app = typer.Typer()


def parse_markdown(markdown_output: str):
    # Ignore all lines before "```python"
    # Ignore all lines after "```"
    # Return everything in between as a single strinbg
    lines = markdown_output.splitlines()
    in_code_block = False
    code_block = ""
    install_cmd = ""
    for line in lines:
        if line == "```python":
            in_code_block = True
        elif line == "```":
            in_code_block = False
        elif line.strip().startswith("#PIPINSTALL"):
            install_cmd = line.strip().split("#PIPINSTALL")[1].strip()
        elif line.strip().startswith("# PIPINSTALL"):
            install_cmd = line.strip().split("# PIPINSTALL")[1].strip()
        elif in_code_block:
            code_block += line + "\n"

    return code_block, install_cmd


@app.command()
def test_gpt_lib(skip_gen: bool = False):
    if skip_gen:
        print("Skipping generation of code, reusing cached code")
    else:
        prompt = "Create a table using rich that shows me the average CPU for each machine, averaged over the past 30 seconds. The url is https://centrality-dev.fly.dev:8000 and the token is 'dev'"
        output = complete(
            model="gpt-4-1106-preview",
            prompt=prompt,
            conversation=[SystemTurn(system_prompt)],
            write_output=True,
        )
        code, pip_install_cmd = parse_markdown(output)
        print(code)
        print(pip_install_cmd)
        write_tmp_and_entrypoint_files(code, install_cmd=pip_install_cmd)
    run_code()


if __name__ == "__main__":
    app()
