import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from vmagent.actors.metrics.samplers.throughput import Throughput
from rich.live import Live
from rich.table import Table
from centrality_controlplane_sdk import Throughput as ThroughputInfo

RecvBandwidthMiB = float
SentBandwidthMiB = float
# InterfaceInfo = tuple[SentBandwidthMiB, RecvBandwidthMiB]


class NetworkSampler(MetricSampler):
    def __init__(self) -> None:
        net = psutil.net_io_counters(pernic=True)
        self.sent = {}
        self.recv = {}
        for interface, net in net.items():
            self.sent[interface] = Throughput(net.bytes_sent)
            self.recv[interface] = Throughput(net.bytes_recv)

    def sample(self) -> dict[str, ThroughputInfo]:
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
                sent_mbps=sent_mib, recv_mbps=recv_mib
            )

        total_sent_mib = sum([info.sent_mbps for info in interface_infos.values()])
        total_recv_mib = sum([info.recv_mbps for info in interface_infos.values()])
        total_info = ThroughputInfo(sent_mbps=total_sent_mib, recv_mbps=total_recv_mib)
        interface_infos["total"] = total_info

        return interface_infos

    def sample_and_render(self, live: Live):
        interface_info = self.sample()
        table = Table()
        header = ["Interface", "Sent MiB/sec", "Recv MiB/sec"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        for interface in interface_info.keys():
            info = interface_info[interface]
            sent = round(info.sent_mbps, 2)
            recv = round(info.recv_mbps, 2)

            table.add_row(interface, str(sent), str(recv))

        live.update(table)
