import os
import typer
import importlib
from rich.console import Console
from scripts.codegen.template_vars import TemplateVars
from scripts.codegen import constants
from scripts.codegen import templating


def codegen(
    template: str,
    console: Console,
    display: bool = False,
) -> None:
    if template not in constants.TEMPLATES:
        raise typer.BadParameter(f"template must be one of {constants.TEMPLATES}")

    if template == "types":
        template_path = constants.TYPES_TEMPLATE
    elif template == "datastore-client":
        template_path = constants.DATASTORE_CLIENT_TEMPLATE
    elif template == "rest":
        template_path = constants.REST_API_TEMPLATE
    else:
        raise ValueError(f"Unknown template: {template}")

    # Load in the variables from the codegenvars files
    var_paths = [
        f
        for f in constants.CODEGENVARS_DIR.glob("*.py")
        if f.is_file() and f.stem != "__init__"
    ]
    var_paths.sort()  # Do the generation in alphabetical order
    template_vars = []
    for var_path in var_paths:
        import_path = f"scripts.codegen.codegenvars.{var_path.stem}"
        vars_module = importlib.import_module(import_path)
        template_vars.append(TemplateVars.from_module(vars_module))
    console.log(
        f"Loaded {len(template_vars)} template vars: [blue]{[v.stem for v in var_paths]}[/blue]"
    )

    # Load in the template
    with open(template_path, "r") as f:
        template_lines = f.readlines()

    # Hydrat the template with the variables
    outputs = []
    for t in template_vars:
        console.log(
            f"Hydrating ./{template_path.relative_to(os.getcwd())} with [blue]{t.metric_name_lowercase}[/blue]"
        )

        output = templating.hydrate_template(
            template_vars=t, template_lines=template_lines
        )

        # There are the type files, write them to files
        if template == "types":
            output_path = (
                constants.TYPES_GENERATED_DIR / f"{t.metric_name_lowercase}.py"
            )

            console.log(
                f"Writing generated code to {output_path.relative_to(os.getcwd())}"
            )
            console.print()
            with open(output_path, "w") as f:
                f.write("\n".join(output))

        outputs.append(output)

    # If this is the datastore client or rest endpoints, we need to combine the outputs and insert them into the
    # implementation files
    outputs_flattened = [item for sublist in outputs for item in sublist]
    if display:
        output_str = "\n".join(outputs_flattened)
        console.print("-" * console.width)
        console.print("Generated code:")
        console.print("-" * console.width)
        console.print(output_str)
    if template == "datastore-client":
        console.log(
            f"Writing generated code to ./{constants.DATASTORE_CLIENT_IMPLEMENTATION.relative_to(os.getcwd())}"
        )
        templating.replace_generated_code(
            file_path=constants.DATASTORE_CLIENT_IMPLEMENTATION,
            new_code=outputs_flattened,
        )
    elif template == "rest":
        console.log(
            f"Writing generated code to ./{constants.REST_API_IMPLEMENTATION.relative_to(os.getcwd())}"
        )
        templating.replace_generated_code(
            file_path=constants.REST_API_IMPLEMENTATION, new_code=outputs_flattened
        )
