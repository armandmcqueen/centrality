from typing import Any

CpuPercents = list[float]


metric_obj_fields = """\
    cpu_percents: list[float]
"""
metric_name_lowercase = "cpu"
metric_name_camelcase = "Cpu"
metric_name_capitalized = "CPU"
metrics_shape_db = "list[float]"
metrics_type_db = "JSONB"
example_metrics = "[cpuWWW, cpuXXX, cpuYYY, cpuZZZ]"
custom_types = "CpuPercents = list[float]"


def convert_from_metrics(metrics: list[float]) -> dict[str, CpuPercents]:
    return dict(cpu_percents=metrics)


def convert_to_metrics(self: Any) -> list[float]:
    return self.cpu_percents
