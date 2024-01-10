import pytest
from scripts.gpt.chats import Chat


def test_clear():
    chat = Chat()
    chat.clear()
    assert len(chat.history) == 0

def test_disable():
    chat = Chat()
    chat.disable()
    assert not chat.config.history_enabled

def test_enable():
    chat = Chat()
    chat.enable()
    assert chat.config.history_enabled

def test_show():
    chat = Chat()
    chat.add_entry("User: Hello")
    chat.add_entry("Assistant: Hi there")
    assert chat.show() == ["User: Hello", "Assistant: Hi there"]

def test_raw():
    chat = Chat()
    chat.add_entry("User: Hello")
    chat.add_entry("Assistant: Hi there")
    assert chat.raw() == "User: Hello\nAssistant: Hi there\n"

def test_config():
    chat = Chat()
    assert chat.config() == "Chat settings"

if __name__ == "__main__":
    pytest.main()
import pytest
from scripts.gpt.chats import Chat
