# Utility functions for asserts with helpful error messages


def list_size(lst: list, expected_size: int):
    assert (
        len(lst) == expected_size
    ), f"Expected list to be of size of {expected_size}, but got {len(lst)}. List: {lst}"


def same_size(lst: list, expected: list):
    assert (
        len(lst) == len(expected)
    ), f"Expected list to be of size of {len(expected)}, but got {len(lst)}. List: {lst}"


def not_empty(lst: list):
    assert (
        len(lst) > 0
    ), f"Expected list to be not empty, but got {len(lst)}. List: {lst}"


def set_equality(lst: list | set, expected: list | set):
    assert set(lst) == set(expected), f"Expected set to be {expected}, but got {lst}"


def list_equality(lst: list, expected: list):
    assert lst == expected, f"Expected list to be {expected}, but got {lst}"


def matches(item1, item2):
    assert item1 == item2, f"Expected {item1} to match {item2}"
