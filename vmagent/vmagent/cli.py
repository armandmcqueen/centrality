import time
import typer
import pykka
import sys
from typing import Annotated

from pathlib import Path

import conclib
from common import constants

from vmagent.config import VmAgentConfig
from vmagent.actorsystem import ActorSystem
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from typing import Optional


app = typer.Typer()


@app.command()
def launch(
        control_plane_host: Optional[str] = None,
        vm_id: Optional[str] = None,
        file: Annotated[Optional[str], typer.Option("--file", "-f")] = None,
):
    """
    Launch the VM Agent actor system, the REST API, and the REST ↔ Actor bridge (using conclib).
    """

    conclib_config = conclib.DefaultConfig()
    config_overrides = dict()
    if vm_id:
        config_overrides["vm_id"]=vm_id
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

    print("🚀 Launching VM Agent actor system")
    # Start conclib bridge
    redis_daemon = conclib.start_redis(config=conclib_config)
    conclib.start_proxy(config=conclib_config)

    print("🚀 Launching VM Agent REST API")
    # Start FastAPI
    config.rest.save_to_envvar()  # Make the rest_config available to the REST API
    api_daemon_thread = conclib.start_api(
        fast_api_command=f"uvicorn vmagent.rest.api:app --port {config.rest.port}",
        healthcheck_url=f"http://localhost:{config.rest.port}{constants.HEALTHCHECK_ENDPOINT}",
        startup_healthcheck_timeout=config.rest.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=config.rest.startup_healthcheck_poll_interval,
    )

    try:
        control_plane_sdk = ControlPlaneSdk(
            config=config.controlplane_sdk,
            token="dev",
        )
        actor_system = ActorSystem(
            vm_agent_config=config,
            control_plane_sdk=control_plane_sdk,
        )
        actor_system.start()

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
        redis_daemon.shutdown()
        api_daemon_thread.shutdown()
        pykka.ActorRegistry.stop_all()
        print("👋 Goodbye")
        return


@app.command()
def hello():
    """ Do nothing command to make typer think there are multiple subcommands"""
    print("Hello")


if __name__ == "__main__":
    app()
