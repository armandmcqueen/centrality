# Utilities for working with dicts. Converting between normal and flattened representations as well as merging.

def flatten_dict(d: dict) -> dict:
    """
    Flatten a nested dict into a flat dict with keys separated by '.'

    NOTE: Fully AI generated code
    """

    def expand(key, value):
        if isinstance(value, dict):
            return [(key + "." + k, v) for k, v in flatten_dict(value).items()]
        else:
            return [(key, value)]

    items = [item for k, v in d.items() for item in expand(k, v)]
    return dict(items)


def test_flatten_dict():
    d = {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3,
            "e": {
                "f": 4,
            },
        },
        "f.g.h": "i",
    }
    assert flatten_dict(d) == {
        "a": 1,
        "b.c": 2,
        "b.d": 3,
        "b.e.f": 4,
        "f.g.h": "i",
    }


def merge_flattened_into_nested(flattened: dict, nested: dict) -> dict:
    """
    Given a flattened dict and a nested dict, merge the flattened dict into the nested
    dict, overwriting values in the nested dict. Pure function, no mutation of inputs.
    """

    out = nested.copy()
    for k, v in flattened.items():
        # Split the key into parts
        parts = k.split(".")
        curr_pointer = out
        # Walk the parts, creating nested dicts as needed
        for part in parts[:-1]:
            if part not in curr_pointer:
                curr_pointer[part] = {}
            curr_pointer = curr_pointer[part]
        # Set the final value
        curr_pointer[parts[-1]] = v
    return out


def test_merge_flattened_into_nested():
    # Test 1
    flattened = {
        "a": 1,
        "b.c": 20,
        "b.d": 30,
        "b.e.f": 4,
        "f.g.h": "i",
    }
    nested = {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3,
            "e": {
                "f": 4,
            },
        },
    }
    expected = {
        "a": 1,
        "b": {
            "c": 20,
            "d": 30,
            "e": {
                "f": 4,
            },
        },
        "f": {
            "g": {
                "h": "i",
            },
        },
    }
    assert merge_flattened_into_nested(flattened, nested) == expected


if __name__ == "__main__":
    test_flatten_dict()
    test_merge_flattened_into_nested()
