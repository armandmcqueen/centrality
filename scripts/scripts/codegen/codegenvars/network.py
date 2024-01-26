from pydantic import BaseModel
from typing import Any

metric_obj_fields = """\
    per_interface: list[Throughput] = Field(..., description="A list with throughput for each network interface. There will be one entry per interface.")
    total: Throughput = Field(..., description="The total throughput for all interfaces summed over all interfaces.")
"""
metric_name_lowercase = "network_throughput"
metric_name_camelcase = "NetworkThroughput"
metric_name_capitalized = "NETWORK_THROUGHPUT"
metrics_shape_db = "dict[str, list[float]]"
metrics_type_db = "JSONB"
example_metrics = "{ifaceA: [sentXXX, recvXXX], ifaceB: [sentYYY, recvYYY], total: [sentZZZ, recvZZZ]}"
custom_types = """\
class Throughput(BaseModel):
    interface_name: str = Field(..., description="The name of the network interface, e.g. eth0.")
    sent_mbps: float = Field(..., description="The sent throughput for the interface in MiB/s.")
    recv_mbps: float = Field(..., description="The received throughput for the interface in MiB/s.")
"""


class Throughput(BaseModel):
    interface_name: str
    sent_mbps: float
    recv_mbps: float


def convert_from_metrics(
    metrics: dict[str, list[float]],
) -> dict[str, list[Throughput] | Throughput]:
    interfaces: list[Throughput] = [
        Throughput(
            interface_name=interface, sent_mbps=throughput[0], recv_mbps=throughput[1]
        )
        for interface, throughput in metrics.items()
        if interface != "total"
    ]
    total = Throughput(
        interface_name="total",
        sent_mbps=metrics["total"][0],
        recv_mbps=metrics["total"][1],
    )
    return dict(per_interface=interfaces, total=total)


def convert_to_metrics(self: Any) -> dict[str, list[float]]:
    return {
        throughput.interface_name: [throughput.sent_mbps, throughput.recv_mbps]
        for throughput in self.per_interface
    }
