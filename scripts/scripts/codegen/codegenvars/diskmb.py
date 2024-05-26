from pydantic import BaseModel
from typing import Any

metric_obj_fields = """\
    usage: dict[str, DiskUsage] = Field(..., description="A dict with disk usage for each disk with the disk name as the key.")
"""
metric_name_lowercase = "disk_usage"
metric_name_camelcase = "DiskUsage"
metric_name_capitalized = "DISK_USAGE"
metrics_shape_db = "dict[str, list[float]]"
metrics_type_db = "JSONB"
example_metrics = "{disk1: [used, total], disk2: [used, total]}"
custom_types = """\
class DiskUsage(BaseModel):
    disk_name: str = Field(..., description="The name of the disk, e.g. /dev/sda.")
    used_mb: float = Field(..., description="The used disk space in MiB.")
    total_mb: float = Field(..., description="The total space of the disk in MiB.")
"""


class DiskUsage(BaseModel):
    disk_name: str
    used_mb: float
    total_mb: float


def convert_from_metrics(
    metrics: dict[str, list[float]],
) -> dict[str, dict[str, DiskUsage]]:
    usage: dict[str, DiskUsage] = {
        disk: DiskUsage(disk_name=disk, used_mb=usage_vals[0], total_mb=usage_vals[1])
        for disk, usage_vals in metrics.items()
    }
    return dict(usage=usage)


def convert_to_metrics(self: Any) -> dict[str, list[float]]:
    output = {}
    for machine_id, usage in self.usage.items():
        output[machine_id] = [usage.used_mb, usage.total_mb]
    return output
