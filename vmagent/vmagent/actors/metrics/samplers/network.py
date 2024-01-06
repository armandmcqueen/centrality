import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from vmagent.actors.metrics.samplers.throughput import Throughput
from rich.live import Live
from rich.table import Table
from dataclasses import dataclass

RecvBandwidthMiB = float
SentBandwidthMiB = float


@dataclass
class InterfaceInfo:
    sent_bandwidth_mib: SentBandwidthMiB
    recv_bandwidth_mib: RecvBandwidthMiB

    def as_tuple(self) -> tuple[SentBandwidthMiB, RecvBandwidthMiB]:
        return self.sent_bandwidth_mib, self.recv_bandwidth_mib


class NetworkSampler(MetricSampler):
    def __init__(self) -> None:
        net = psutil.net_io_counters(pernic=True)
        self.sent = {}
        self.recv = {}
        for interface, net in net.items():
            self.sent[interface] = Throughput(net.bytes_sent)
            self.recv[interface] = Throughput(net.bytes_recv)

    def sample(self) -> dict[str, InterfaceInfo]:
        interface_infos = {}
        net_per_iface = psutil.net_io_counters(pernic=True)
        for interface, net in net_per_iface.items():
            if interface == "lo":
                continue

            # nics could be added
            if interface not in self.sent or interface not in self.recv:
                self.sent[interface] = Throughput(net.bytes_sent)
                self.recv[interface] = Throughput(net.bytes_recv)
                # Skip on this iteration because we don't have a previous value to compare to
                continue

            recv_mib = self.recv[interface].add(net.bytes_recv) / 1024 / 1024
            sent_mib = self.sent[interface].add(net.bytes_sent) / 1024 / 1024
            info = InterfaceInfo(
                sent_bandwidth_mib=sent_mib, recv_bandwidth_mib=recv_mib
            )
            interface_infos[interface] = info

        total_sent_mib = sum(
            [info.sent_bandwidth_mib for info in interface_infos.values()]
        )
        total_recv_mib = sum(
            [info.recv_bandwidth_mib for info in interface_infos.values()]
        )
        total_info = InterfaceInfo(
            sent_bandwidth_mib=total_sent_mib, recv_bandwidth_mib=total_recv_mib
        )
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
            sent, recv = interface_info[interface].as_tuple()
            sent = round(sent, 2)
            recv = round(recv, 2)

            table.add_row(interface, str(sent), str(recv))

        live.update(table)


def main():
    sampler = NetworkSampler()
    val = sampler.sample()
    print(val)


if __name__ == "__main__":
    main()
