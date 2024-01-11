from rich import print
from rich.console import Console
from rich.live import Live
import time
from vmagent.actors.metrics.samplers.cpu import CpuSampler
from vmagent.actors.metrics.samplers.diskio import DiskIoSampler
from vmagent.actors.metrics.samplers.diskmb import DiskMbSampler
from vmagent.actors.metrics.samplers.gpu import GpuSampler
from vmagent.actors.metrics.samplers.memory import MemorySampler
from vmagent.actors.metrics.samplers.network import NetworkSampler
from vmagent.actors.metrics.samplers.nvidia_smi import NvidiaSmiSampler

import typer

app = typer.Typer()


def loop_and_render(metric_sampler, refresh_rate=10):
    console = Console()
    try:
        with Live(
            console=console, refresh_per_second=refresh_rate, transient=True
        ) as live:
            while True:
                metric_sampler.sample_and_render(live)
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("[red]Aborted")

    metric_sampler.shutdown()


@app.command(
    help="Collect and render real-time metrics from a given metric sampler",
)
def main(
    sampler: str = typer.Argument(
        ...,
        help="The metric sampler to use. Valid options are: gpu, diskio, diskmb, network (aka: net), cpu, memory (aka: mem), nvidia-smi",
    ),
    refresh_rate: int = typer.Option(10, help="The refresh rate in Hz"),
):
    if sampler == "gpu":
        metric_sampler = GpuSampler()
    elif sampler == "diskio":
        metric_sampler = DiskIoSampler()
    elif sampler == "diskmb":
        metric_sampler = DiskMbSampler()
    elif sampler == "network" or sampler == "net":
        metric_sampler = NetworkSampler()
    elif sampler == "cpu":
        metric_sampler = CpuSampler()
    elif sampler == "memory" or sampler == "mem":
        metric_sampler = MemorySampler()
    elif sampler == "nvidia-smi":
        metric_sampler = NvidiaSmiSampler()
    else:
        raise typer.BadParameter("Invalid collector")

    loop_and_render(metric_sampler, refresh_rate)


if __name__ == "__main__":
    app()
