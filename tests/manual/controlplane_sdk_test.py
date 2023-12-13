import datetime

from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from common.sdks.controlplane.handwritten.config import DefaultControlPlaneSdkConfig, ControlPlaneSdkConfig
from common.types.vmmetrics import CpuMeasurement
import time
import rich
from rich.progress import Progress
from rich.spinner import Spinner

console = rich.console.Console()



def test_sdk(config: ControlPlaneSdkConfig, token: str):
    client = ControlPlaneSdk(config=config, token=token)

    # TODO: Tests are too fast for this spinner to be useful, but keeping
    #       it around for now as reference
    with console.status(spinner="aesthetic", status="[bold cyan]Running tests...", spinner_style="bold cyan") as status:
        response = client.get_healthcheck()
        if response.status_code != 200:
            console.print("[bold red]Healthcheck failed")
            rich.inspect(response)
            return
        else:
            console.print("[bold green]Healthcheck passed")

        response = client.get_auth_healthcheck()
        if response.status_code != 200:
            console.print("[bold red]Auth healthcheck failed")
            rich.inspect(response)
            return
        else:
            console.print("[bold green]Auth healthcheck passed")


        vm_id = "sdk-examplevm"
        measurement = CpuMeasurement(
            vm_id=vm_id,
            ts=datetime.datetime.utcnow(),
            cpu_percents=[1.0, 2.0, 3.0],
        )
        response = client.write_cpu_metric(measurement=measurement)
        if response.status_code != 200:
            console.print("[bold red]Write CPU metric failed")
            rich.inspect(response)
            return
        else:
            console.print("[bold green]Write CPU metric passed")

        response, measurements = client.get_cpu_measurements(vm_ids=[vm_id])
        if response.status_code != 200:
            console.print("[bold red]Get CPU metric failed")
            rich.inspect(response)
            return
        else:

            console.print("[bold green]Get CPU metric passed")


if __name__ == '__main__':
    config = DefaultControlPlaneSdkConfig()
    token = "dev"

    test_sdk(config, token)
