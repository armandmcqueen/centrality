# File to save a config and conversation history
from pathlib import Path
import uuid
from dataclasses import dataclass, asdict
from typing import Optional
import json

CONFIG_DIR = Path("~/.gptutils").expanduser()

SYSTEM_PROMPT = (
    "Please generate the shortest answer you can that is informative. "
    "This will be displayed directly in the terminal. The ideal output "
    "is one line of code and one line describing what the command does. "
    "Less than 5 is still good. Remember, this will be displayed directly "
    "in the terminal, so do not include markdown formatting and code to be "
    "run directly should on its own line. It's really important that we don't"
    "have markdown codeblocks that use backticks (` or ```)."
)
SYSTEM_PROMPT_PROPOSE = (
    "Please generate a one-line bash command as well as one or more comment lines. This will be presented to the user"
    "as a suggestion and then automatically executed. It's really important that we don't"
    "have markdown codeblocks that use backticks (` or ```). If you want to include a comment,"
    "please use a #. It is absolutely essential that the command is one line and that anything"
    "that is not code is a comment."
)


@dataclass
class ChatEntry:
    response: str

    def as_json(self):
        raise NotImplementedError()

    @property
    def role(self):
        raise NotImplementedError()

    def __str__(self):
        return f"[{self.role}]\n{self.response}"


@dataclass
class AssistantTurn(ChatEntry):
    def as_json(self):
        return {"role": "assistant", "content": self.response}

    @property
    def role(self):
        return "Assistant"


@dataclass
class UserTurn(ChatEntry):
    def as_json(self):
        return {"role": "user", "content": self.response}

    @property
    def role(self):
        return "User"


@dataclass
class ChatConfig:
    history_on: bool = True
    chat_system_prompt: str = SYSTEM_PROMPT
    chatx_system_prompt: str = SYSTEM_PROMPT_PROPOSE


def pop_next_entry(lines: list[str], expected_uuid):
    assert lines[0] == expected_uuid, f"Expected {expected_uuid} but got {lines[0]}"
    lines.pop(0)
    role = lines.pop(0)
    response = ""
    while len(lines) > 0 and lines[0] != expected_uuid:
        response += lines.pop(0) + "\n"

    if role == "[User]":
        return UserTurn(response)
    else:
        return AssistantTurn(response)


class ConversationHistory:
    def __init__(self, history_file: Path):
        self.history_file = history_file
        if not history_file.exists():
            history_file.touch()
            history_file.write_text(f"{uuid.uuid4()}\n")

        # Parse the history file
        history_lines = history_file.read_text().splitlines()
        # The first line is always the UUID
        self.uuid = history_lines.pop(0)
        self.history: list[ChatEntry] = []

        # Delete all the lines at the end that are empty
        while len(history_lines) > 0 and history_lines[-1] == "":
            history_lines.pop()

        # Extract entry by entry, mutating history_lines until it is empty
        while len(history_lines) > 0:
            next_entry = pop_next_entry(history_lines, self.uuid)
            self.history.append(next_entry)

    def add_entry(self, entry: ChatEntry):
        self.history.append(entry)
        with self.history_file.open("a") as f:
            f.write(self.uuid)
            f.write("\n")
            f.write(f"[{entry.role}]\n")
            trimmed_response = entry.response.rstrip("\n")
            f.write(f"{trimmed_response}\n")

    def clear(self):
        self.history = []
        self.history_file.write_text(self.uuid)


class Chat:
    def _init_(self, configdir: Path = CONFIG_DIR, history_id: Optional[str] = None):
        self.configdir = configdir
        if not configdir.exists():
            configdir.mkdir(parents=True)
        if not configdir.is_dir():
            raise ValueError(f"{configdir} is not a directory")

        self.history_file = configdir / "history.txt"
        if history_id:
            self.history_file = configdir / f"history-{history_id}.txt"
        self.config_file = configdir / "config.json"

        if not self.config_file.exists():
            config = ChatConfig()
            self._save_config(config)

        with self.config_file.open("r") as f:
            config = ChatConfig(**json.load(f))

        self.config = config
        self.history_holder = ConversationHistory(self.history_file)

    def _save_config(self, config: ChatConfig):
        with self.config_file.open("w") as f:
            json.dump(asdict(config), f)

    @property
    def history(self) -> list[ChatEntry]:
        if self.config.history_on:
            return self.history_holder.history
        return []

    @property
    def history_file_contents(self):
        return self.history_file.read_text()

    def add_entry(self, entry: ChatEntry):
        if self.config.history_on:
            self.history_holder.add_entry(entry)

    def clear_history(self):
        self.history_holder.clear()

    def disable_history(self):
        self.config.history_on = False
        with self.config_file.open("w") as f:
            json.dump(asdict(self.config), f)

    def enable_history(self):
        self.config.history_on = True
        with self.config_file.open("w") as f:
            json.dump(asdict(self.config), f)

    def set_chat_system_prompt(self, prompt: str):
        self.config.chat_system_prompt = prompt
        self._save_config(self.config)

    def set_chatx_system_prompt(self, prompt: str):
        self.config.chatx_system_prompt = prompt
        self._save_config(self.config)

    def display_config(self):
        for k, v in asdict(self.config).items():
            print(f"{k}: {v}")
