import pytest
from scripts.gpt.lib import complete, run_interactive


def test_complete():
    # Test case 1: Empty conversation
    prompt = "Hello"
    model = "gpt-4-1106-preview"
    conversation = []
    write_output = True
    result = complete(prompt, model, conversation, write_output)
    assert result == ""

    # Test case 2: Non-empty conversation
    prompt = "Hello"
    model = "gpt-4-1106-preview"
    conversation = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    write_output = True
    result = complete(prompt, model, conversation, write_output)
    assert result == "Assistant: Hi there"

def test_run_interactive():
    # Test case 1: Empty history
    model = "gpt-4-1106-preview"
    result = run_interactive(model)
    assert result == ""

    # Test case 2: Non-empty history
    model = "gpt-4-1106-preview"
    result = run_interactive(model)
    assert result == ""

if __name__ == "__main__":
    pytest.main()
