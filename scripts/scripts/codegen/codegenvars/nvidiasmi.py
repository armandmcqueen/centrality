from typing import Any


metric_obj_fields = """\
    output: str
"""
metric_name_lowercase = "nvidia_smi"
metric_name_camelcase = "NvidiaSmi"
metric_name_capitalized = "NVIDIA_SMI"
metrics_shape_db = "str"
metrics_type_db = "String"
example_metrics = "N/A"
custom_types = ""


def convert_from_metrics(metrics: str) -> dict[str, str]:
    return dict(output=metrics)


def convert_to_metrics(self: Any) -> str:
    return self.output
