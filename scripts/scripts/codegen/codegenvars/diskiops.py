from typing import Any
from pydantic import BaseModel

metric_obj_fields = """\
    iops: list[DiskIops]
"""
metric_name_lowercase = "disk_iops"
metric_name_camelcase = "DiskIops"
metric_name_capitalized = "DISK_IOPS"
metrics_shape_db = "dict[str, float]"
metrics_type_db = "JSONB"
example_metrics = "{disk1: iopsXXX, disk2: iopsYYY}"
custom_types = """\
class DiskIops(BaseModel):
    disk_name: str
    iops: float
"""


class DiskIops(BaseModel):
    disk_name: str
    iops: float


def convert_from_metrics(metrics: dict[str, float]) -> dict[str, list[DiskIops]]:
    iops: list[DiskIops] = [
        DiskIops(disk_name=device, iops=iops_val)
        for device, iops_val in metrics.items()
    ]
    return dict(iops=iops)


def convert_to_metrics(self: Any) -> dict[str, float]:
    iops = {}
    for iop in self.iops:
        iops[iop.disk_name] = iop.iops
    return iops
