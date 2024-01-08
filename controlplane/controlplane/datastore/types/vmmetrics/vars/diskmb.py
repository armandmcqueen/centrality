from pydantic import BaseModel

metric_obj_fields = """\
    usage: dict[str, DiskUsage]
"""
metric_name_lowercase = "disk_usage"
metric_name_camelcase = "DiskUsage"
metrics_shape_db = "dict[str, list[float]]"
example_metrics = "{disk1: [used, total], disk2: [used, total]}"
custom_types = """\
class DiskUsage(BaseModel):
    used_mb: float
    total_mb: float
"""


class DiskUsage(BaseModel):
    used_mb: float
    total_mb: float


def convert(metrics: dict[str, list[float]]) -> dict[str, dict[str, DiskUsage]]:
    usage: dict[str, DiskUsage] = {
        disk: DiskUsage(used_mb=usage_vals[0], total_mb=usage_vals[1])
        for disk, usage_vals in metrics.items()
    }
    return dict(usage=usage)
