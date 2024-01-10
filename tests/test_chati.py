import pytest
from scripts.gpt.chat import Chat


def test_clear_history():
    chat = Chat()
    chat.clear_history()
    assert len(chat.history) == 0


def test_disable_history():
    chat = Chat()
    chat.disable_history()
    assert not chat.config.history_enabled


def test_enable_history():
    chat = Chat()
    chat.enable_history()
    assert chat.config.history_enabled


def test_add_entry():
    chat = Chat()
    chat.add_entry("User: Hello")
    assert len(chat.history) == 1
    assert chat.history[0] == "User: Hello"


def test_history_file_contents():
    chat = Chat()
    chat.add_entry("User: Hello")
    chat.add_entry("Assistant: Hi there")
    assert chat.history_file_contents == "User: Hello\nAssistant: Hi there\n"


if __name__ == "__main__":
    pytest.main()
