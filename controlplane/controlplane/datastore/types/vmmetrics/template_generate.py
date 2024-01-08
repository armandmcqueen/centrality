from pathlib import Path

template = Path(__file__).parent / "template.py"
generated_dir = Path(__file__).parent / "generated"


def generate_template(tvars):
    metric_obj_fields = tvars.metric_obj_fields
    metric_name_lowercase = tvars.metric_name_lowercase
    metric_name_camelcase = tvars.metric_name_camelcase
    metrics_shape_db = tvars.metrics_shape_db
    convert_fn_str = inspect.getsource(tvars.convert)
    example_metrics = tvars.example_metrics
    custom_types = tvars.custom_types

    with open(template, "r") as f:
        template_str = f.read()

    template_str = template_str.replace("#CONVERT", convert_fn_str)
    template_str = template_str.replace("#EXAMPLE_METRICS", example_metrics)
    template_str = template_str.replace("#METRIC_OBJ_FIELDS", metric_obj_fields)
    template_str = template_str.replace("#CUSTOMTYPES", custom_types)
    template_str = template_str.replace("METRIC_NAME_LOWERCASE", metric_name_lowercase)
    template_str = template_str.replace("METRIC_NAME_CAMELCASE", metric_name_camelcase)
    template_str = template_str.replace("METRIC_SHAPE_DB", metrics_shape_db)

    output_path = generated_dir / f"{metric_name_lowercase}.py"
    # print(template_str)
    with open(output_path, "w") as f:
        f.write(template_str)


if __name__ == "__main__":
    import importlib
    import inspect
    from rich import print

    # tvars_file = "memory.py"
    for tvars_file in [
        "cpu.py",
        "diskiops.py",
        "diskmb.py",
        "diskthroughput.py",
        "gpumemory.py",
        "gpuutilization.py",
        "memory.py",
        "network.py",
    ]:
        tvars_file_path = Path(__file__).parent / "vars" / tvars_file
        print(f"Generating {tvars_file_path}")
        tvars = importlib.import_module(
            f"controlplane.datastore.types.vmmetrics.vars.{tvars_file[:-3]}"
        )
        # richinspect(tvars)

        generate_template(tvars)
