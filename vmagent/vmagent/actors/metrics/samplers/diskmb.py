import psutil
from actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live

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
        # TODO: Implement
        pass
