from common.sdks.controlplane.sdk import get_sdk
from common.cli_utils import CliContextManager
from common import constants
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.text import Text
import rich
import typer
import time


app = typer.Typer()


@app.command()
def watch_vms() -> None:
    control_plane_sdk_config = ControlPlaneSdkConfig()
    sdk = get_sdk(
        config=control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    rich.print("[bold underline cyan]Active Machines")
    text = Text()

    with CliContextManager():
        with Live(text, refresh_per_second=10) as live:
            tick_count = 0  # ticks are 1/1000 of a second
            loop_interval_ticks = 100
            while True:
                if tick_count % 200 == 0:
                    # Update the list of VMs we track
                    live_vms = sdk.list_live_vms()
                    text = Text("\n".join(live_vms))
                    live.update(text)

                if tick_count % 100 == 0:
                    # TODO: Update the color of the listing based on time since last heartbeat
                    pass

                time.sleep(loop_interval_ticks / 1000)
                tick_count += loop_interval_ticks


@app.command()
def watch_cpu() -> None:
    control_plane_sdk_config = ControlPlaneSdkConfig()
    sdk = get_sdk(
        config=control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )

    console = rich.console.Console()

    def get_progress_descriptions(vm_id: str) -> str:
        return f"[cyan]VM {vm_id}"

    with CliContextManager():
        console.print("[bold underline cyan]Active Machines CPU")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            refresh_per_second=10,
        ) as progress:
            vm_bars = {}
            live_vms = sdk.list_live_vms()
            # TODO: Handle errors?
            for vm_id in live_vms:
                vm_bars[vm_id] = progress.add_task(
                    get_progress_descriptions(vm_id), total=100
                )

            tick_count = 0  # ticks are 1/1000 of a second
            loop_interval_ticks = 100

            while True:
                if tick_count % 10_000 == 0:
                    # Update the list of VMs we track
                    live_vms = sdk.list_live_vms()
                    # TODO: Handle errors?
                    new_set = set(live_vms)
                    old_set = set(vm_bars.keys())
                    vms_to_add = new_set - old_set
                    vms_to_remove = old_set - new_set
                    for vm_id in vms_to_add:
                        vm_bars[vm_id] = progress.add_task(
                            get_progress_descriptions(vm_id), total=100
                        )
                    for vm_id in vms_to_remove:
                        progress.remove_task(vm_bars[vm_id])
                        del vm_bars[vm_id]

                if tick_count % 200 == 0:
                    # Update the CPU metrics for all VMs current tracked
                    live_vms = list(vm_bars.keys())
                    if len(live_vms) != 0:
                        latest_cpu_measurements = sdk.get_latest_cpu_metrics(
                            vm_ids=live_vms
                        )
                        # TODO: Handle errors?

                        for measurement in latest_cpu_measurements:
                            avg_cpu_percent = sum(measurement.cpu_percents) / len(
                                measurement.cpu_percents
                            )
                            progress.update(
                                vm_bars[measurement.vm_id], completed=avg_cpu_percent
                            )

                time.sleep(loop_interval_ticks / 1000)
                tick_count += loop_interval_ticks


if __name__ == "__main__":
    app()
