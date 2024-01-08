metric_obj_fields = """\
    gpu_percents: list[float]
"""
metric_name_lowercase = "gpu_utilization"
metric_name_camelcase = "GpuUtilization"
metrics_shape_db = "list[float]"
example_metrics = "[20, 40, 60, 80]"
custom_types = """\
"""


# Types to make convert() valid python
def convert(metrics: list[float]) -> dict[str, list[float]]:
    return dict(gpu_percents=metrics)
