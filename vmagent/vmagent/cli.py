import time
import typer
import pykka

import conclib
from common import constants

from vmagent.rest.config import VmAgentRestConfig, DefaultVmAgentRestConfig
from vmagent.actorsystem import ActorSystem
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig, DefaultControlPlaneSdkConfig
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk


app = typer.Typer()


def get_default_configs() -> tuple[
    conclib.ConclibConfig,
    VmAgentRestConfig,
    ControlPlaneSdkConfig,
]:
    conclib_config = conclib.DefaultConfig()
    rest_config = DefaultVmAgentRestConfig()
    control_plane_sdk_config = DefaultControlPlaneSdkConfig()
    return conclib_config, rest_config, control_plane_sdk_config


@app.command()
def launch():
    """
    Launch the VM Agent actor system, the REST API, and the REST ↔ Actor bridge (using conclib).
    """
    conclib_config, rest_config, control_plane_sdk_config = get_default_configs()
    # TODO: Proper token and device id
    vm_id = "test-machine-2"

    # Start conclib bridge
    redis_daemon = conclib.start_redis(config=conclib_config)
    conclib.start_proxy(config=conclib_config)

    # Start FastAPI
    rest_config.save_to_envvar()  # Make the rest_config available to the REST API
    api_daemon_thread = conclib.start_api(
        fast_api_command=f"uvicorn vmagent.rest.api:app --port {rest_config.port}",
        healthcheck_url=f"http://localhost:{rest_config.port}{constants.HEALTHCHECK_ENDPOINT}",
        startup_healthcheck_timeout=rest_config.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=rest_config.startup_healthcheck_poll_interval,
    )

    try:
        control_plane_sdk = ControlPlaneSdk(
            config=control_plane_sdk_config,
            token="dev",
        )
        actor_system = ActorSystem(
            vm_id=vm_id,
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
