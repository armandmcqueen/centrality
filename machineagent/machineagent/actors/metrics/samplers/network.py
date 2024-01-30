import psutil
from machineagent.actors.metrics.samplers.sampler import MetricSampler
from machineagent.actors.metrics.samplers.throughput import Throughput
from rich.live import Live
from rich.table import Table
from centrality_controlplane_sdk import Throughput as ThroughputInfo

RecvBandwidthMiB = float
SentBandwidthMiB = float
TotalThroughputInfo = ThroughputInfo
# InterfaceInfo = tuple[SentBandwidthMiB, RecvBandwidthMiB]


class NetworkSampler(MetricSampler):
    def __init__(self) -> None:
        net = psutil.net_io_counters(pernic=True)
        self.sent = {}
        self.recv = {}
        for interface, net in net.items():
            self.sent[interface] = Throughput(net.bytes_sent)
            self.recv[interface] = Throughput(net.bytes_recv)

    def sample(self) -> tuple[dict[str, ThroughputInfo], TotalThroughputInfo]:
        interface_infos = {}
        net_per_iface = psutil.net_io_counters(pernic=True)
        for interface, net in net_per_iface.items():
            # nics could be added
            if interface not in self.sent or interface not in self.recv:
                self.sent[interface] = Throughput(net.bytes_sent)
                self.recv[interface] = Throughput(net.bytes_recv)
                # Skip on this iteration because we don't have a previous value to compare to
                continue

            recv_mib = self.recv[interface].add(net.bytes_recv) / 1024 / 1024
            sent_mib = self.sent[interface].add(net.bytes_sent) / 1024 / 1024
            interface_infos[interface] = ThroughputInfo(
                interface_name=interface, sent_mbps=sent_mib, recv_mbps=recv_mib
            )

        total_sent_mib = sum([info.sent_mbps for name, info in interface_infos.items()])
        total_recv_mib = sum([info.recv_mbps for name, info in interface_infos.items()])
        total_info = ThroughputInfo(
            interface_name="total", sent_mbps=total_sent_mib, recv_mbps=total_recv_mib
        )
        interface_infos["total"] = total_info

        return interface_infos, total_info

    def sample_and_render(self, live: Live):
        interface_infos, total_info = self.sample()

        def clean(xx_mbps):
            return str(round(xx_mbps, 2))

        table = Table()
        header = ["Interface", "Sent MiB/sec", "Recv MiB/sec"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        table.add_row(
            total_info.interface_name,
            clean(total_info.sent_mbps),
            clean(total_info.recv_mbps),
        )
        for name, info in interface_infos.items():
            if info.interface_name == "total":
                continue
            sent = round(info.sent_mbps, 2)
            recv = round(info.recv_mbps, 2)

            table.add_row(info.interface_name, str(sent), str(recv))

        live.update(table)
