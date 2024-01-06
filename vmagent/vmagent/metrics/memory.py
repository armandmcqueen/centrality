import psutil
from vmagent.metrics.collector import MetricCollector
from rich.live import Live

FreeMemoryMiB = float


class MemoryCollector(MetricCollector):
    def collect(self) -> FreeMemoryMiB:
        free_memory_mib = psutil.virtual_memory().available / 1024 / 1024
        return free_memory_mib

    def collect_and_render(self, live: Live):
        free_memory = self.collect()
        free_memory = int(free_memory)
        live.update(f"Free Memory: {free_memory} MiB")
