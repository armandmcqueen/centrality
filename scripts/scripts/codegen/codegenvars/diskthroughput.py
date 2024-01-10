from pydantic import BaseModel
from typing import Any

metric_obj_fields = """\
    throughput: list[DiskThroughput]
"""
metric_name_lowercase = "disk_throughput"
metric_name_camelcase = "DiskThroughput"
metric_name_capitalized = "DISK_THROUGHPUT"
metrics_shape_db = "dict[str, list[float]]"
example_metrics = "{disk1: [read, write], disk2: [read, write]}"
custom_types = """\
class DiskThroughput(BaseModel):
    disk_name: str
    read_mbps: float
    write_mbps: float
"""


class DiskThroughput(BaseModel):
    disk_name: str
    read_mbps: float
    write_mbps: float


def convert_from_metrics(
    metrics: dict[str, list[float]],
) -> dict[str, list[DiskThroughput]]:
    throughput: list[DiskThroughput] = [
        DiskThroughput(
            disk_name=disk, read_mbps=throughput_vals[0], write_mbps=throughput_vals[1]
        )
        for disk, throughput_vals in metrics.items()
    ]
    return dict(throughput=throughput)


def convert_to_metrics(self: Any) -> dict[str, list[float]]:
    return {
        throughput.disk_name: [throughput.read_mbps, throughput.write_mbps]
        for throughput in self.throughput
    }
