import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from vmagent.actors.metrics.samplers.throughput import Throughput
from centrality_controlplane_sdk import DiskThroughput as DiskThroughputHolder
from centrality_controlplane_sdk import DiskIops as DiskIopsHolder
from rich.live import Live
from rich.table import Table

DiskThroughputs = list[DiskThroughputHolder]
IopsPerDisk = list[DiskIopsHolder]


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

    def sample(self) -> tuple[DiskThroughputs, IopsPerDisk]:
        throughputs = []
        iopses = []
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
            throughputs.append(
                DiskThroughputHolder(
                    disk_name=disk_name, read_mbps=read_mb, write_mbps=write_mb
                )
            )
            iopses.append(DiskIopsHolder(disk_name=disk_name, iops=iops))
        return throughputs, iopses

    def sample_and_render(self, live: Live):
        # Write each disk's throughput and IOPS as a row
        # TODO: Fix this
        throughputs, iops = self.sample()

        table = Table()
        header = ["Disk", "Read MiB/sec", "Write MiB/sec", "IOPS"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        table.add_column(header[3])

        iops_by_disk = {i.disk_name: i for i in iops}
        for t in throughputs:
            disk_iops = iops_by_disk[t.disk_name]
            read_mib = int(t.read_mbps)
            write_mib = int(t.write_mbps)
            disk_iops = int(disk_iops.iops)
            table.add_row(t.disk_name, str(read_mib), str(write_mib), str(disk_iops))
        live.update(table)
