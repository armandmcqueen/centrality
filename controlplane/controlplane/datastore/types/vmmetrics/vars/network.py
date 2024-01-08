from pydantic import BaseModel

metric_obj_fields = """\
    per_interface: dict[str, Throughput]
    total: Throughput
"""
metric_name_lowercase = "network_throughput"
metric_name_camelcase = "NetworkThroughput"
metrics_shape_db = "dict[str, list[float]]"
example_metrics = "{ifaceA: [sentXXX, recvXXX], ifaceB: [sentYYY, recvYYY], total: [sentZZZ, recvZZZ]}"
custom_types = """\
class Throughput(BaseModel):
    sent_mbps: float
    recv_mbps: float
"""


class Throughput(BaseModel):
    sent_mbps: float
    recv_mbps: float


def convert(
    metrics: dict[str, list[float]],
) -> dict[str, dict[str, Throughput] | Throughput]:
    interfaces: dict[str, Throughput] = {
        interface: Throughput(sent_mbps=throughput[0], recv_mbps=throughput[1])
        for interface, throughput in metrics.items()
        if interface != "total"
    }
    total = Throughput(sent_mbps=metrics["total"][0], recv_mbps=metrics["total"][1])
    return dict(per_interface=interfaces, total=total)
