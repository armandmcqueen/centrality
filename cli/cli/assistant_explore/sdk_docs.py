import git  # TODO: Add to requirements.txt
from pathlib import Path
from rich import print
import tiktoken  # TODO: Add to requirements.txt?

SDK_DIR = (
    Path(git.Repo(".", search_parent_directories=True).working_tree_dir)
    / "sdk_controlplane"
)
DOCS_FILE = Path(__file__).parent / "docs.md"


def main():
    docs = [SDK_DIR / "README.md"]
    for file in SDK_DIR.glob("docs/*.md"):
        docs.append(file)

    all_text = ""
    for file in docs:
        all_text += "---\n\n"
        contents = file.read_text()
        all_text += contents
    all_text += "\n\n"

    with DOCS_FILE.open("w") as f:
        f.write(all_text)

    print(f"Got all docs from {len(docs)} files. Total length: {len(all_text)}")

    # Count number of tokens via tiktoken
    token_count = len(tiktoken.get_encoding("cl100k_base").encode(all_text))
    print(f"Number of tokens: {token_count}")


if __name__ == "__main__":
    main()
