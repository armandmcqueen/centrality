import psutil
from actors.metrics.samplers.sampler import MetricSampler
from actors.metrics.samplers.throughput import Throughput
from rich.live import Live

ReadThroughputMiB = float
WriteThroughputMiB = float
Iops = float
ThroughputInfos = dict[str, tuple[ReadThroughputMiB, WriteThroughputMiB]]
IopsInfos = dict[str, Iops]


class DiskIoSampler(MetricSampler):
    def __init__(self):
        disks = psutil.disk_io_counters(perdisk=True)
        self.read = {}
        self.write = {}
        self.iops = {}
        for disk_name, disk in disks.items():
            self.read[disk_name] = Throughput(disk.read_bytes)
            self.write[disk_name] = Throughput(disk.write_bytes)
            self.iops[disk_name] = Throughput(disk.read_count + disk.write_count)

    def sample(self) -> tuple[ThroughputInfos, IopsInfos]:
        disk_throughput_infos = {}
        disk_iops_infos = {}
        disks = psutil.disk_io_counters(perdisk=True)
        for disk_name, disk in disks.items():
            # Disks could be added?
            if disk_name not in self.read or disk_name not in self.write:
                self.read[disk_name] = Throughput(disk.read_bytes)
                self.write[disk_name] = Throughput(disk.write_bytes)
                self.iops[disk_name] = Throughput(disk.read_count + disk.write_count)
                # Skip on this iteration because we don't have a previous value to compare to
                continue

            read = self.read[disk_name].add(disk.read_bytes) / 1024 / 1024
            write = self.write[disk_name].add(disk.write_bytes) / 1024 / 1024
            iops = self.iops[disk_name].add(disk.read_count + disk.write_count)
            disk_throughput_infos[disk_name] = (read, write)
            disk_iops_infos[disk_name] = iops
        return disk_throughput_infos, disk_iops_infos

    def sample_and_render(self, live: Live):
        # TODO: Rewrite collect_and_render
        pass
        # read, write, iops = self.collect()
        # read_mib = round(read, 2)
        # write_mib = round(write, 2)
        # iops = round(iops, 2)
        # live.update(
        #     f"Read MiB/sec: {read_mib}\nWrite MiB/sec: {write_mib}\nIOPS: {iops}"
        # )
