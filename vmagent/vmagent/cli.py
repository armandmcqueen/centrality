import time
import typer
import pykka
import socket
from typing import Annotated

from pathlib import Path

import conclib
import urllib3.exceptions

from common import constants

from vmagent.config import VmAgentConfig
from vmagent.actorsystem import VmAgentActorSystem
from common.sdks.controlplane.sdk import get_sdk
from typing import Optional
from centrality_controlplane_sdk import DataApi

MAX_CONTROL_PLANE_WAIT_TIMEOUT = 60

app = typer.Typer()


class ControlPlaneUnavailableError(Exception):
    pass


def wait_for_control_plane_healthy(control_plane_sdk: DataApi, timeout_secs: int):
    max_time = time.time() + MAX_CONTROL_PLANE_WAIT_TIMEOUT
    while time.time() < max_time:
        try:
            control_plane_sdk.get_healthcheck()
            break

        except Exception as e:
            if not isinstance(e, urllib3.exceptions.MaxRetryError):
                print(
                    f"Unexpected error while waiting for control plane to be ready: {e}"
                )
            print(
                f"❗ Control plane health check not passing. Time until timeout: {max_time - time.time()}"
            )
            time.sleep(1)
    else:
        raise ControlPlaneUnavailableError(
            f"❌️ Control Plane failed to have passing healthcheck after {MAX_CONTROL_PLANE_WAIT_TIMEOUT} seconds"
        )


@app.command()
def launch(
    control_plane_host: Optional[str] = None,
    vm_id: Optional[str] = None,
    file: Annotated[Optional[str], typer.Option("--file", "-f")] = None,
):
    """
    Launch the VM Agent actor system, the REST API, and the REST ↔ Actor bridge (using conclib).

    If vm_id == "auto", the hostname will be used as the vm_id.
    """

    conclib_config = conclib.DefaultConfig()
    config_overrides = dict()
    if vm_id:
        if vm_id == "auto":  # TODO: Document this
            print("🙈 Overriding vm_id with hostname")
            vm_id = f"auto-{socket.gethostname()}"

        config_overrides["vm_id"] = vm_id
    if control_plane_host:
        config_overrides["controlplane_sdk"] = dict(host=control_plane_host)

    if file:
        file = Path(file)
        print(f"💾 Loading config from {file.resolve().absolute()}")
        config = VmAgentConfig.from_yaml_file(file, config_overrides=config_overrides)
    else:
        print("🌱 Using default configs")
        config = VmAgentConfig(config_overrides=config_overrides)

    print("⚙️ Config:")
    config.pretty_print_yaml()

    print("🚀 Launching conclib proxy")
    redis_daemon = conclib.start_redis(config=conclib_config)
    conclib.start_proxy(config=conclib_config)
    print("✓ conclib proxy launched")

    print("💤 Waiting for control plane to be ready")
    control_plane_sdk = get_sdk(
        config.controlplane_sdk, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    wait_for_control_plane_healthy(control_plane_sdk, MAX_CONTROL_PLANE_WAIT_TIMEOUT)
    print("✓ Control plane is ready")

    print("🚀 Launching VM Agent actor system")
    _ = VmAgentActorSystem(
        vm_agent_config=config,
        control_plane_sdk=control_plane_sdk,
    ).start()
    print("✓ VM Agent actor system launched")

    print("🚀 Launching VM Agent REST API")
    # Start FastAPI
    config.rest.save_to_envvar()  # Make the rest_config available to the REST API
    api_daemon_thread = conclib.start_api(
        fast_api_command=f"uvicorn vmagent.rest.api:app --port {config.rest.port}",
        healthcheck_url=f"http://localhost:{config.rest.port}{constants.HEALTHCHECK_ENDPOINT}",
        startup_healthcheck_timeout=config.rest.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=config.rest.startup_healthcheck_poll_interval,
    )
    print("✓ VM Agent REST API launched")

    try:
        # Wait until something fails or the user kills the process
        while True:
            time.sleep(100)

    except KeyboardInterrupt:
        print()  # Print a newline to make the output look nicer after ^C
        print("🛑 KeyboardInterrupt encountered, shutting down REST API")
    except Exception as e:
        print(e)
        print(f"❗️Control Plane API shutting down due to {type(e)} exception")
    finally:
        api_daemon_thread.shutdown()
        pykka.ActorRegistry.stop_all()
        redis_daemon.shutdown()
        print("👋 Goodbye")
        return


@app.command()
def hello():
    """Do nothing command to make typer think there are multiple subcommands"""
    print("Hello")


if __name__ == "__main__":
    app()
