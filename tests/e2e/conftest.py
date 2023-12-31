import pytest
import subprocess
from pathlib import Path
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig
from common.utils.wait_for_healthy import wait_for_healthy
from common import constants
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
def sdk(sdk_config):
    """Make the SDK available to all tests, pointed at the compose stack"""
    sdk = ControlPlaneSdk(
        config=sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    return sdk


@pytest.fixture(scope="session")
def docker_compose(sdk):
    """
    Start the Docker Compose stack, wait for it to be healthy, and clean up after tests are done.

    Saves logs to a file. Corrects for some common errors:
    - Check if docker compose stack is already running and shut it down if so
    - Check if `docker compose build` needs to be run.
        TODO: This should be smarter, currently just runs build if compose up fails
    """
    print()
    print("Ensuring Docker Compose stack is not currently running")
    subprocess.run("docker compose down", shell=True, check=True)

    def docker_compose_up():
        subprocess.run(
            f"docker compose -f {compose_file_path.absolute()} -f {compose_override_file_path.absolute()} up -d",
            shell=True,
            check=True,
        )

    try:
        docker_compose_up()
    except subprocess.CalledProcessError as e:
        print(e)
        print("[bold red]Docker Compose failed to start. Retrying after a rebuild.")
        subprocess.run("docker compose build", shell=True, check=True)
        docker_compose_up()

    wait_for_healthy(
        healthcheck_url=sdk._build_url(constants.HEALTHCHECK_ENDPOINT),  # noqa
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
        resp, live_vms = sdk.get_live_vms()
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
    subprocess.run("docker compose down", shell=True, check=True)
