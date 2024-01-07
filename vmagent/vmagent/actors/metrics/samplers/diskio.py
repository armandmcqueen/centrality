
import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from vmagent.actors.metrics.samplers.throughput import Throughput
from rich.live import Live
from rich.table import Table

ReadThroughputMiB = float
WriteThroughputMiB = float
Iops = float
ThroughputInfos = dict[str, tuple[ReadThroughputMiB, WriteThroughputMiB]]
IopsInfos = dict[str, Iops]


class DiskIoSampler(MetricSampler):
    def __init__(self):
        disks = psutil.disk_io_counters(perdisk=True)
        self.read_trackers = {}
        self.write_trackers = {}
        self.iops_trackers = {}
        for disk_name, disk in disks.items():
            self.read_trackers[disk_name] = Throughput(disk.read_bytes)
            self.write_trackers[disk_name] = Throughput(disk.write_bytes)
            self.iops_trackers[disk_name] = Throughput(
                disk.read_count + disk.write_count
            )

    def sample(self) -> tuple[ThroughputInfos, IopsInfos]:
        throughputs = {}
        iopses = {}
        disks = psutil.disk_io_counters(perdisk=True)
        for disk_name, disk in disks.items():
            # Disks could be added
            if (
                disk_name not in self.read_trackers
                or disk_name not in self.write_trackers
            ):
                self.read_trackers[disk_name] = Throughput(disk.read_bytes)
                self.write_trackers[disk_name] = Throughput(disk.write_bytes)
                self.iops_trackers[disk_name] = Throughput(
                    disk.read_count + disk.write_count
                )
                # Skip on this iteration because we don't have a previous value to compare to
                continue

            read_mb = self.read_trackers[disk_name].add(disk.read_bytes) / 1024 / 1024
            write_mb = (
                self.write_trackers[disk_name].add(disk.write_bytes) / 1024 / 1024
            )
            iops = self.iops_trackers[disk_name].add(disk.read_count + disk.write_count)
            throughputs[disk_name] = (read_mb, write_mb)
            iopses[disk_name] = iops
        return throughputs, iopses

    def sample_and_render(self, live: Live):
        # Write each disk's throughput and IOPS as a row
        throughput, iops = self.sample()
        disk_ids = throughput.keys()

        table = Table()
        header = ["Disk", "Read MiB/sec", "Write MiB/sec", "IOPS"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        table.add_column(header[3])

        for disk_id in disk_ids:
            read, write = throughput[disk_id]
            disk_iops = iops[disk_id]
            read_mib = int(read)
            write_mib = int(write)
            disk_iops = int(disk_iops)
            table.add_row(disk_id, str(read_mib), str(write_mib), str(disk_iops))
        live.update(table)
