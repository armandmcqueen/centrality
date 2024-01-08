metric_obj_fields = """\
    free_memory_mb: float
    total_memory_mb: float
"""
metric_name_lowercase = "memory"
metric_name_camelcase = "Memory"
metrics_shape_db = "list[float]"
example_metrics = "[1000, 2000]"
custom_types = ""


def convert(metrics: list[float]) -> dict[str, float]:
    free_memory_mb = metrics[0]
    total_memory_mb = metrics[1]
    return dict(free_memory_mb=free_memory_mb, total_memory_mb=total_memory_mb)
