from rich import print
from rich.console import Console
from rich.live import Live
import time
from vmagent.metrics.gpu import GpuCollector
from vmagent.metrics.disk import DiskCollector
from vmagent.metrics.net import NetCollector
from vmagent.metrics.cpu import CpuCollector
from vmagent.metrics.memory import MemoryCollector

import typer

app = typer.Typer()


def loop_and_render(metric_collector, refresh_rate=10):
    console = Console()
    try:
        with Live(
            console=console, refresh_per_second=refresh_rate, transient=True
        ) as live:
            while True:
                metric_collector.collect_and_render(live)
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("[red]Aborted")

    metric_collector.shutdown()


@app.command()
def main(
    collector: str = typer.Argument(
        ...,
        help="The metric collector to use. Valid options are: gpu, disk, network (aka: net), cpu, memory (aka: mem)",
    ),
    refresh_rate: int = typer.Option(10, help="The refresh rate in Hz"),
):
    if collector == "gpu":
        metric_collector = GpuCollector()
    elif collector == "disk":
        metric_collector = DiskCollector()
    elif collector == "network" or collector == "net":
        metric_collector = NetCollector()
    elif collector == "cpu":
        metric_collector = CpuCollector()
    elif collector == "memory" or collector == "mem":
        metric_collector = MemoryCollector()
    else:
        raise typer.BadParameter("Invalid collector")

    loop_and_render(metric_collector, refresh_rate)


if __name__ == "__main__":
    app()
