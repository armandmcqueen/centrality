import subprocess

from machineagent.actors.metrics.samplers.sampler import MetricSampler
from rich.live import Live


class NvidiaSmiSampler(MetricSampler):
    def sample(self) -> str:
        out = subprocess.check_output("nvidia-smi", shell=True)
        return out.decode("utf-8")

    def sample_and_render(self, live: Live):
        out = self.sample()
        live.update(out)
