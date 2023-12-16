from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
import rich
import typer
import time


app = typer.Typer()


def get_default_configs() -> ControlPlaneSdkConfig:
    return ControlPlaneSdkConfig()


@app.command()
def watch_cpu_metrics():
    control_plane_sdk_config = get_default_configs()
    token = "dev"
    control_plane_sdk = ControlPlaneSdk(
        config=control_plane_sdk_config,
        token=token,
    )

    console = rich.console.Console()

    def get_progress_descriptions(vm_id: str):
        return f"[cyan]VM {vm_id}"

    try:
        console.print("[bold underline cyan]Active Machines")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            vm_bars = {}
            resp, live_vms = control_plane_sdk.get_live_vms()
            # TODO: Handle errors?
            for vm_id in live_vms:
                vm_bars[vm_id] = progress.add_task(
                    get_progress_descriptions(vm_id), total=100
                )

            sec_count = 0
            loop_interval = 0.5
            while True:
                if sec_count % 10 == 0:
                    # Update the list of VMs we track
                    resp, live_vms = control_plane_sdk.get_live_vms()
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

                if sec_count % 1 == 0:
                    # Update the CPU metrics for all VMs current tracked
                    live_vms = list(vm_bars.keys())
                    if len(live_vms) != 0:
                        (
                            resp,
                            latest_cpu_measurements,
                        ) = control_plane_sdk.get_latest_cpu_measurements(live_vms)
                        # TODO: Handle errors?

                        for measurement in latest_cpu_measurements:
                            avg_cpu_percent = sum(measurement.cpu_percents) / len(
                                measurement.cpu_percents
                            )
                            progress.update(
                                vm_bars[measurement.vm_id], completed=avg_cpu_percent
                            )

                time.sleep(loop_interval)
                sec_count += loop_interval

    except KeyboardInterrupt:
        print("🛑 Received keyboard interrupt.")
        return
    except Exception as e:
        print("❗️ Encountered an error")
        print(e)
    finally:
        print("👋 Goodbye")


if __name__ == "__main__":
    app()
