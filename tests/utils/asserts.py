# Utility functions for asserts with helpful error messages


def pretty_str_list(lst: list):
    # Being with a newline and have each entry separated by a newline
    return "\n" + "\n".join([str(x) for x in lst])


def list_size(lst: list, expected_size: int):
    assert (
        len(lst) == expected_size
    ), f"Expected list to be of size of {expected_size}, but got {len(lst)}. List: {pretty_str_list(lst)}"


def same_size(lst: list, expected: list):
    assert (
        len(lst) == len(expected)
    ), f"Expected list to be of size of {len(expected)}, but got {len(lst)}. List: {pretty_str_list(lst)}. \nExpected: {pretty_str_list(expected)}"


def not_empty(lst: list):
    assert (
        len(lst) > 0
    ), f"Expected list to be not empty, but got {len(lst)}. List: {pretty_str_list(lst)}"


def set_equality(lst: list | set, expected: list | set):
    assert (
        set(lst) == set(expected)
    ), f"Expected set to be {pretty_str_list(expected)}\n, but got {pretty_str_list(lst)}"


def list_equality(lst: list, expected: list):
    assert (
        lst == expected
    ), f"Expected list to be {pretty_str_list(expected)}\n, but got {pretty_str_list(lst)}"


def matches(item1, item2):
    assert item1 == item2, f"Expected {item1} to match {item2}"
