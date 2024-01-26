from typing import Any
from pydantic import BaseModel

metric_obj_fields = """\
    iops: list[DiskIops] = Field(..., description="A list with IOPS for each disk. Each disk will have one entry in the list.")
"""
metric_name_lowercase = "disk_iops"
metric_name_camelcase = "DiskIops"
metric_name_capitalized = "DISK_IOPS"
metrics_shape_db = "dict[str, float]"
metrics_type_db = "JSONB"
example_metrics = "{disk1: iopsXXX, disk2: iopsYYY}"
custom_types = """\
class DiskIops(BaseModel):
    disk_name: str = Field(..., description="The name of the disk, e.g. /dev/sda.")
    iops: float = Field(..., description="The IOPS for the disk.")
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
