import os
import typer
from rich import print

app = typer.Typer()


def update_dependency(
    file_path: str, dependency_name: str, old_version: str, new_version: str
):
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated = False
    old_line = None
    new_line = None
    for i, line in enumerate(lines):
        raw_line = line.strip().replace("'", "").replace('"', "")
        if (
            raw_line.startswith(f"{dependency_name} ==")
            or raw_line.startswith(f"{dependency_name} ~=")
            or raw_line.startswith(f"{dependency_name} >=")
        ):
            if old_version in line:
                old_line = line
                lines[i] = line.replace(old_version, new_version)
                new_line = lines[i]
                updated = True
                break

    if updated:
        print(f"Updating {file_path}: {old_line.strip()} -> {new_line.strip()}")
        confirm = input("Apply this change? (y/n): ")
        if confirm.lower() == "y":
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            print("Changes applied.")
        else:
            print("No changes made.")


@app.command()
def upgrade(
    dependency_name: str,
    old_version: str,
    new_version: str,
):
    for subdir, dirs, files in os.walk("."):
        for file in files:
            if file == "pyproject.toml":
                file_path = os.path.join(subdir, file)
                if ".ignore" in file_path:
                    continue
                print(file_path)
                update_dependency(file_path, dependency_name, old_version, new_version)


if __name__ == "__main__":
    app()
