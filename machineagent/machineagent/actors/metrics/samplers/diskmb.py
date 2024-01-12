import psutil
from machineagent.actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live
from rich.table import Table
from centrality_controlplane_sdk import DiskUsage as DiskUsageHolder


class DiskMbSampler(MetricSampler):
    def sample(self) -> list[DiskUsageHolder]:
        usages = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # This can happen if the disk isn't ready
                continue

            total_mb = usage.total / (1024 * 1024)
            used_mb = usage.used / (1024 * 1024)
            usages.append(
                DiskUsageHolder(
                    disk_name=partition.device, used_mb=used_mb, total_mb=total_mb
                )
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
        for usage in info:
            used = int(usage.used_mb)
            total = int(usage.total_mb)
            percent = round(used / total * 100, 2)
            table.add_row(usage.disk_name, str(used), str(total), str(percent) + "%")

        live.update(table)
