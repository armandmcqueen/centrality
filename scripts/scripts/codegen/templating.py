from enum import Enum
from pathlib import Path
from scripts.codegen import constants
from scripts.codegen.template_vars import TemplateVars


class State(Enum):
    BEFORE = 0
    BETWEEN = 1
    AFTER = 2


BeforeLines = list[str]
AfterLines = list[str]


def remove_lines_between_strings(
    lines: list[str], start_sentinel: str, end_sentinel: str
) -> tuple[BeforeLines, AfterLines]:
    # NOTE: keeps the sentinel lines in before and after

    # Confirm that both the start and end sentinel are in the list exactly once or error out
    start_count = sum([1 for line in lines if start_sentinel in line])
    end_count = sum([1 for line in lines if end_sentinel in line])
    if start_count != 1 or end_count != 1:
        raise ValueError(
            f"Expected exactly one {start_sentinel=} and one {end_sentinel=} "
            f"in the file, found {start_count} start and {end_count} end"
        )

    before, after = [], []
    state = State.BEFORE
    for line in lines:
        if start_sentinel in line:
            state = State.BETWEEN
            before.append(line)
        elif end_sentinel in line:
            state = State.AFTER
            after.append(line)
        elif state == State.BEFORE:
            before.append(line)
        elif state == State.AFTER:
            after.append(line)
    return before, after


def replace_generated_code(file_path: Path, new_code: list[str]) -> None:
    with open(file_path, "r") as f:
        starting_lines = f.readlines()

    before, after = remove_lines_between_strings(
        starting_lines, constants.BEGIN_SENTINEL, constants.END_SENTINEL
    )
    all_lines = []
    all_lines.extend(before)
    all_lines.extend(new_code)
    all_lines.extend(after)

    # Remove trailing newlines from all lines
    all_lines = [line.rstrip() for line in all_lines]

    with open(file_path, "w") as f:
        for line in all_lines:
            f.write(line + "\n")


def remove_lines_before_string(lines, search_string):
    # Find the index of the line containing the string
    index = None
    for i, line in enumerate(lines):
        if search_string in line:
            index = i + 1
            break

    # If the string is not found, return the original list
    if index is None:
        return lines

    # Return the list from the found index onwards
    return lines[index:]


def hydrate_template(
    template_vars: TemplateVars, template_lines: list[str]
) -> list[str]:
    ignore_before_str = "#PRETEMPLATE_END"
    template_lines = remove_lines_before_string(template_lines, ignore_before_str)

    template_str = "".join(template_lines)
    template_str = template_str.replace(
        "#CONVERTFROMMETRICS", template_vars.convert_from_metrics_fn_str
    )
    template_str = template_str.replace(
        "#CONVERTTOMETRICS", template_vars.convert_to_metrics_fn_str
    )
    template_str = template_str.replace(
        "#EXAMPLE_METRICS", template_vars.example_metrics
    )
    template_str = template_str.replace(
        "#METRIC_OBJ_FIELDS", template_vars.metric_obj_fields
    )
    template_str = template_str.replace("#CUSTOMTYPES", template_vars.custom_types)

    template_str = template_str.replace(
        "METRIC_NAME_LOWERCASE", template_vars.metric_name_lowercase
    )
    template_str = template_str.replace(
        "METRIC_NAME_CAMELCASE", template_vars.metric_name_camelcase
    )
    template_str = template_str.replace(
        "METRIC_NAME_CAPITALIZED", template_vars.metric_name_capitalized
    )
    template_str = template_str.replace(
        "METRIC_SHAPE_DB", template_vars.metrics_shape_db
    )

    lines = template_str.splitlines()
    return lines
