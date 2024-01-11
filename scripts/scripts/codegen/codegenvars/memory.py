from typing import Any

metric_obj_fields = """\
    free_memory_mb: float
    total_memory_mb: float
"""
metric_name_lowercase = "memory"
metric_name_camelcase = "Memory"
metric_name_capitalized = "MEMORY"
metrics_shape_db = "list[float]"
metrics_type_db = "JSONB"
example_metrics = "[1000, 2000]"
custom_types = ""


def convert_from_metrics(metrics: list[float]) -> dict[str, float]:
    free_memory_mb = metrics[0]
    total_memory_mb = metrics[1]
    return dict(free_memory_mb=free_memory_mb, total_memory_mb=total_memory_mb)


def convert_to_metrics(self: Any) -> list[float]:
    return [self.free_memory_mb, self.total_memory_mb]
