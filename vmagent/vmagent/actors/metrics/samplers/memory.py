import psutil
from vmagent.actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live

FreeMemoryMiB = float
TotalMemoryMiB = float


class MemorySampler(MetricSampler):
    def sample(self) -> tuple[FreeMemoryMiB, TotalMemoryMiB]:
        free_memory_mib = psutil.virtual_memory().available / 1024 / 1024
        total_memory_mib = psutil.virtual_memory().total / 1024 / 1024
        return free_memory_mib, total_memory_mib

    def sample_and_render(self, live: Live):
        free_memory_mib, total_memory_mib = self.sample()
        free_memory_mib = int(free_memory_mib)
        live.update(
            f"Free Memory: {free_memory_mib} MiB\nTotal Memory: {total_memory_mib} MiB"
        )
