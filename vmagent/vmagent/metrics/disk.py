import psutil
from vmagent.metrics.collector import MetricCollector
from vmagent.metrics.throughput import Throughput
from rich.live import Live

ReadThroughputMiB = float
WriteThroughputMiB = float
Iops = float


class DiskCollector(MetricCollector):
    def __init__(self):
        disk = psutil.disk_io_counters()
        self.read = Throughput(disk.read_bytes)
        self.write = Throughput(disk.write_bytes)
        self.iops = Throughput(disk.read_count + disk.write_count)

    def collect(self) -> tuple[ReadThroughputMiB, WriteThroughputMiB, Iops]:
        disk = psutil.disk_io_counters()
        read = self.read.add(disk.read_bytes) / 1024 / 1024
        write = self.write.add(disk.write_bytes) / 1024 / 1024
        iops = self.iops.add(disk.read_count + disk.write_count)
        return read, write, iops

    def collect_and_render(self, live: Live):
        read, write, iops = self.collect()
        read_mib = round(read, 2)
        write_mib = round(write, 2)
        iops = round(iops, 2)
        live.update(
            f"Read MiB/sec: {read_mib}\nWrite MiB/sec: {write_mib}\nIOPS: {iops}"
        )
