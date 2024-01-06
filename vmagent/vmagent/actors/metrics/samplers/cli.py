from rich import print
from rich.console import Console
from rich.live import Live
import time
from actors.metrics.samplers.gpu import GpuSampler
from actors.metrics.samplers.diskio import DiskIoCollector
from actors.metrics.samplers.net import NetworkSampler
from actors.metrics.samplers.cpu import CpuSampler
from actors.metrics.samplers.memory import MemorySampler

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
    collector: str = typer.Argument(
        ...,
        help="The metric collector to use. Valid options are: gpu, disk, network (aka: net), cpu, memory (aka: mem)",
    ),
    refresh_rate: int = typer.Option(10, help="The refresh rate in Hz"),
):
    if collector == "gpu":
        metric_collector = GpuSampler()
    elif collector == "disk":
        metric_collector = DiskIoCollector()
    elif collector == "network" or collector == "net":
        metric_collector = NetworkSampler()
    elif collector == "cpu":
        metric_collector = CpuSampler()
    elif collector == "memory" or collector == "mem":
        metric_collector = MemorySampler()
    else:
        raise typer.BadParameter("Invalid collector")

    loop_and_render(metric_collector, refresh_rate)


if __name__ == "__main__":
    app()
