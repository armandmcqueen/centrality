import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live
from rich.table import Table
from pydantic import BaseModel

UsedMiB = float
TotalMiB = float
DiskPartition = str


class DiskMbInfo(BaseModel):
    used_mb: UsedMiB
    total_mb: TotalMiB


class DiskMbSampler(MetricSampler):
    def sample(self) -> dict[DiskPartition, DiskMbInfo]:
        usages = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # This can happen if the disk isn't ready
                continue

            total_mb = usage.total / (1024 * 1024)
            used_mb = usage.used / (1024 * 1024)
            usages[partition.mountpoint] = DiskMbInfo(
                used_mb=used_mb, total_mb=total_mb
            )
        return usages

    def sample_and_render(self, live: Live):
        info = self.sample()
        table = Table()
        header = ["Disk", "Used MiB", "Total MiB", "Percent Used"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        table.add_column(header[3])
        for disk_id in info.keys():
            used = int(info[disk_id].used_mb)
            total = int(info[disk_id].total_mb)
            percent = round(used / total * 100, 2)
            table.add_row(disk_id, str(used), str(total), str(percent) + "%")

        live.update(table)
