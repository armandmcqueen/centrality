import psutil
from vmagent.metrics.collector import MetricCollector
from rich.live import Live


class CpuCollector(MetricCollector):
    def collect(self) -> list[float]:
        cpu_utils = psutil.cpu_percent(percpu=True)
        return cpu_utils

    def collect_and_render(self, live: Live):
        cpu_utils = self.collect()
        cpu_util_str = [f"{round(cpu_util, 2)}%" for cpu_util in cpu_utils]
        # Make sure all strings are the same length
        max_len = 6
        cpu_util_str = [cpu_util.rjust(max_len) for cpu_util in cpu_util_str]
        avg = int(sum(cpu_utils) / len(cpu_utils))
        avg_str = f"{avg}%".rjust(3)
        live.update(f"CPU Util: {cpu_util_str}\nAvg CPU Util: {avg_str}")
