import os
import typer
from rich import print
import git

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
        confirm = input("Apply this change? (Y/n): ")
        if confirm.lower() == "y" or confirm == "":
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            print("Changes applied.")
        else:
            print("No changes made.")
    else:
        print(f"Dependency {dependency_name} {old_version} not found")


@app.command()
def upgrade(
    dependency_name: str,
    old_version: str,
    new_version: str,
):
    repo_root = git.Repo(".", search_parent_directories=True)
    # Wall all files recursively starting from the repo root
    for subdir, dirs, files in os.walk(repo_root.working_tree_dir):
        for file in files:
            if file == "pyproject.toml":
                file_path = os.path.join(subdir, file)
                if ".ignore" in file_path:
                    continue
                print()
                print(f"Checking {file_path}")
                update_dependency(file_path, dependency_name, old_version, new_version)


if __name__ == "__main__":
    app()
