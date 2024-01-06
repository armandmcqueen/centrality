import psutil
from vmagent.metrics.collector import MetricCollector
from vmagent.metrics.throughput import Throughput
from rich.live import Live

RecvBandwidthMiB = float
SentBandwidthMiB = float


class NetCollector(MetricCollector):
    def __init__(self) -> None:
        net = psutil.net_io_counters()
        self.sent = Throughput(net.bytes_sent)
        self.recv = Throughput(net.bytes_recv)

    def collect(self) -> tuple[SentBandwidthMiB, RecvBandwidthMiB]:
        net = psutil.net_io_counters()
        sent_mib = self.sent.add(net.bytes_sent) / 1024 / 1024
        recv_mib = self.recv.add(net.bytes_recv) / 1024 / 1024
        return sent_mib, recv_mib

    def collect_and_render(self, live: Live):
        sent, recv = self.collect()
        sent_mib = round(sent, 2)
        recv_mib = round(recv, 2)
        live.update(f"Sent MiB/sec: {sent_mib}\nRecv MiB/sec: {recv_mib}")
