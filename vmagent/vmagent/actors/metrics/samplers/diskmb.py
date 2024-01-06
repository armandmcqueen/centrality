import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live
from rich.table import Table

UsedMiB = float
TotalMiB = float
DiskMbInfo = tuple[UsedMiB, TotalMiB]


class DiskMbSampler(MetricSampler):
    def sample(self) -> dict[str, DiskMbInfo]:
        info = {}
        for partition in psutil.disk_partitions():
            try:
                # Get partition usage
                usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # This can happen if the disk isn't ready
                continue

            total_mb = usage.total / (1024 * 1024)
            used_mb = usage.used / (1024 * 1024)
            info[partition.mountpoint] = (used_mb, total_mb)
        return info

    def sample_and_render(self, live: Live):
        info = self.sample()
        table = Table()
        header = ["Disk", "Used MiB", "Total MiB", "Percent Used"]
        table.add_column(header[0])
        table.add_column(header[1])
        table.add_column(header[2])
        for disk_id in info.keys():
            used, total = info[disk_id]
            used = int(used)
            total = int(total)
            percent = round(used / total * 100, 2)
            table.add_row(disk_id, str(used), str(total), str(percent) + "%")

        live.update(table)
