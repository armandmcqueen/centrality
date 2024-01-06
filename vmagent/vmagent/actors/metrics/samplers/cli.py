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
    help="Collect and render real-time metrics from a given metric collector",
)
def main(
    sampler: str = typer.Argument(
        ...,
        help="The metric sampler to use. Valid options are: gpu, diskio, diskmb, network (aka: net), cpu, memory (aka: mem)",
    ),
    refresh_rate: int = typer.Option(10, help="The refresh rate in Hz"),
):
    if sampler == "gpu":
        metric_collector = GpuSampler()
    elif sampler == "diskio":
        metric_collector = DiskIoSampler()
    elif sampler == "diskmb":
        metric_collector = DiskMbSampler()
    elif sampler == "network" or sampler == "net":
        metric_collector = NetworkSampler()
    elif sampler == "cpu":
        metric_collector = CpuSampler()
    elif sampler == "memory" or sampler == "mem":
        metric_collector = MemorySampler()
    else:
        raise typer.BadParameter("Invalid collector")

    loop_and_render(metric_collector, refresh_rate)


if __name__ == "__main__":
    app()
