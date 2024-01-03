import pytest
import subprocess
from pathlib import Path
from centrality_controlplane_sdk import DataApi
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig
from common.utils.wait_for_healthy import wait_for_healthy
from common import constants
from common.sdks.controlplane.sdk import get_sdk
from rich import print
import time


compose_file_path = Path(__file__).parent.parent.parent / "compose.yaml"
compose_override_file_path = (
    Path(__file__).parent.parent.parent / "compose-override-mountcode.yaml"
)
logs_file_path = Path(__file__).parent / "docker_logs.txt"


@pytest.fixture(scope="session")
def sdk_config():
    config = ControlPlaneSdkConfig()
    return config


@pytest.fixture(scope="session")
def sdk(sdk_config) -> DataApi:
    """Make the SDK available to all tests, pointed at the compose stack"""
    client = get_sdk(sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN)
    return client


@pytest.fixture(scope="session")
def unauthed_sdk(sdk_config) -> DataApi:
    """Make an unauthorized SDK available"""
    client = get_sdk(
        sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN, disable_auth=True
    )
    return client


@pytest.fixture(scope="session")
def docker_compose(sdk: DataApi, sdk_config: ControlPlaneSdkConfig):
    """
    Start the Docker Compose stack, wait for it to be healthy, and clean up after tests are done.

    Saves logs to a file. Corrects for some common errors:
    - Check if docker compose stack is already running and shut it down if so
    - Check if `docker compose build` needs to be run.
        TODO: This should be smarter, currently just runs build if compose up fails
    """
    print()
    print("Ensuring Docker Compose stack is not currently running")
    subprocess.run("docker compose down --timeout 1", shell=True, check=True)

    def docker_compose_up():
        subprocess.run(
            f"docker compose -f {compose_file_path.absolute()} -f {compose_override_file_path.absolute()} up -d",
            shell=True,
            check=True,
        )

    try:
        print("Launching docker compose")
        docker_compose_up()
    except subprocess.CalledProcessError as e:
        print(e)
        print("[bold red]Docker Compose failed to start. Retrying after a rebuild.")
        subprocess.run("docker compose build", shell=True, check=True)
        docker_compose_up()

    scheme = "https" if sdk_config.https else "http"
    healthcheck_url = f"{scheme}://{sdk_config.host}:{sdk_config.port}{constants.HEALTHCHECK_ENDPOINT}"
    wait_for_healthy(
        healthcheck_url=healthcheck_url,
        startup_healthcheck_timeout=120,
        startup_healthcheck_poll_interval=0.5,
        log_progress=True,
        suppress_error=False,
    )

    # Wait for the agents to send heartbeats
    max_time = time.time() + 20
    while True:
        if time.time() > max_time:
            raise Exception(
                "Timed out waiting for live vms endpoint to show 4 machines"
            )
        live_vms = sdk.list_live_vms()
        if len(live_vms) == 4:
            print("Live vms endpoint shows 4 machines as expected.")
            break
        else:
            print(
                f"Waiting for live vms endpoint to show 4 machines, currently {len(live_vms)}"
            )
        time.sleep(0.5)

    print("[green bold]Compose stack is ready for testing")

    # Yield to allow tests to run
    yield

    # Teardown: Stop Docker Compose and gather logs
    subprocess.run(f"docker compose logs > {logs_file_path}", shell=True, check=True)
    print(f"\n\nLogs written to {logs_file_path}")
    print("Tearing down Docker Compose stack")
    subprocess.run("docker compose down --timeout 1", shell=True, check=True)
