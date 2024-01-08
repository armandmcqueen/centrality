import os
from pathlib import Path
from dataclasses import dataclass
import typer
import importlib
import inspect
from rich.console import Console
from enum import Enum

# TODO: This whole file could use a cleanup

app = typer.Typer()

console = Console()

templates = ["types", "datastore-client", "rest"]

types_template = Path(__file__).parent / "datastore/types/vmmetrics/types.template"
datastore_client_template = Path(__file__).parent / "datastore/client.template"
datastore_client_implementation = Path(__file__).parent / "datastore/client.py"
rest_api_template = Path(__file__).parent / "rest/rest.template"
rest_api_implementation = Path(__file__).parent / "rest/api.py"

# TODO: Move generated directory to here

BEGIN_SENTINEL = "# BEGIN GENERATED CODE"
END_SENTINEL = "# END GENERATED CODE"


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


class State(Enum):
    BEFORE = 0
    BETWEEN = 1
    AFTER = 2


BeforeLines = list[str]
AfterLines = list[str]


def remove_lines_between_strings(
    lines: list[str], start_sentinel: str, end_sentinel: str
) -> tuple[BeforeLines, AfterLines]:
    # Keeps the sentinel lines in before and after

    # Confirm that both the start and end sentinel are in the list exactly once or error
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
        starting_lines, BEGIN_SENTINEL, END_SENTINEL
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


@dataclass
class TemplateVars:
    metric_obj_fields: str
    metric_name_lowercase: str
    metric_name_camelcase: str
    metric_name_capitalized: str
    metrics_shape_db: str
    example_metrics: str
    custom_types: str
    convert_from_metrics_fn_str: str
    convert_to_metrics_fn_str: str


def hydrate_template(
    vars: TemplateVars, template_lines: list[str], display: bool = False
) -> list[str]:
    ignore_before_str = "#PRETEMPLATE_END"
    template_lines = remove_lines_before_string(template_lines, ignore_before_str)

    template_str = "".join(template_lines)
    template_str = template_str.replace(
        "#CONVERTFROMMETRICS", vars.convert_from_metrics_fn_str
    )
    template_str = template_str.replace(
        "#CONVERTTOMETRICS", vars.convert_to_metrics_fn_str
    )
    template_str = template_str.replace("#EXAMPLE_METRICS", vars.example_metrics)
    template_str = template_str.replace("#METRIC_OBJ_FIELDS", vars.metric_obj_fields)
    template_str = template_str.replace("#CUSTOMTYPES", vars.custom_types)

    template_str = template_str.replace(
        "METRIC_NAME_LOWERCASE", vars.metric_name_lowercase
    )
    template_str = template_str.replace(
        "METRIC_NAME_CAMELCASE", vars.metric_name_camelcase
    )
    template_str = template_str.replace(
        "METRIC_NAME_CAPITALIZED", vars.metric_name_capitalized
    )
    template_str = template_str.replace("METRIC_SHAPE_DB", vars.metrics_shape_db)
    if display:
        console.print(template_str)

    lines = template_str.splitlines()
    return lines


@app.command()
def main(template: str, display: bool = False) -> None:
    if template not in templates:
        raise typer.BadParameter(f"template must be one of {templates}")

    if template == "types":
        template_path = types_template
    elif template == "datastore-client":
        template_path = datastore_client_template
    elif template == "rest":
        template_path = rest_api_template
    else:
        raise NotImplementedError()

    codegenvars_dir = Path(__file__).parent / "codegenvars"
    var_paths = [f for f in codegenvars_dir.glob("*.py") if f.is_file()]
    var_paths.sort()

    outputs = []
    for vars_file_path in var_paths:
        # If we are outputting the generated code, the visual dividers are nice. Otherwise they are clutter
        if display:
            console.print("-" * console.width)
        console.print(
            f"Hydrating ./{template_path.relative_to(os.getcwd())} with [blue]{vars_file_path.stem}[/blue]"
        )
        if display:
            console.print("-" * console.width)
        import_path = f"controlplane.codegenvars.{vars_file_path.stem}"
        # print("import", import_path)
        vars_module = importlib.import_module(import_path)

        vars = TemplateVars(
            metric_obj_fields=vars_module.metric_obj_fields,
            metric_name_lowercase=vars_module.metric_name_lowercase,
            metric_name_camelcase=vars_module.metric_name_camelcase,
            metric_name_capitalized=vars_module.metric_name_capitalized,
            metrics_shape_db=vars_module.metrics_shape_db,
            example_metrics=vars_module.example_metrics,
            custom_types=vars_module.custom_types,
            convert_from_metrics_fn_str=inspect.getsource(
                vars_module.convert_from_metrics
            ),
            convert_to_metrics_fn_str=inspect.getsource(vars_module.convert_to_metrics),
        )
        # print(vars)
        with open(template_path, "r") as f:
            template_lines = f.readlines()
        output = hydrate_template(
            vars=vars, template_lines=template_lines, display=display
        )

        # There are the type files, write them to files
        if template == "types":
            output_path = (
                Path(__file__).parent
                / f"datastore/types/vmmetrics/generated/{vars.metric_name_lowercase}.py"
            )
            console.print(
                f"Writing generated code to {output_path.relative_to(os.getcwd())}"
            )
            console.print()
            with open(output_path, "w") as f:
                f.write("\n".join(output))

        outputs.append(output)

    outputs_flattened = [item for sublist in outputs for item in sublist]
    if display:
        output_str = "\n".join(outputs_flattened)
        console.print("-" * console.width)
        console.print("Generated code:")
        console.print("-" * console.width)
        console.print(output_str)
    if template == "datastore-client":
        console.print(
            f"Writing generated code to ./{datastore_client_implementation.relative_to(os.getcwd())}"
        )
        replace_generated_code(
            file_path=datastore_client_implementation, new_code=outputs_flattened
        )
    elif template == "rest":
        console.print(
            f"Writing generated code to ./{rest_api_implementation.relative_to(os.getcwd())}"
        )
        replace_generated_code(
            file_path=rest_api_implementation, new_code=outputs_flattened
        )


if __name__ == "__main__":
    app()
