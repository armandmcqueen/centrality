import time
import typer
import pykka

import conclib
from common import constants

from vmagent.rest.config import VmAgentRestConfig, DefaultVmAgentRestConfig


app = typer.Typer()


def get_default_configs() -> tuple[conclib.ConclibConfig, VmAgentRestConfig]:
    conclib_config = conclib.DefaultConfig()
    rest_config = DefaultVmAgentRestConfig()
    return conclib_config, rest_config


@app.command()
def launch():
    """
    Launch the VM Agent actor system, the REST API, and the REST ↔ Actor bridge (using conclib).
    """
    conclib_config, rest_config = get_default_configs()
    rest_config.save_to_envvar()

    fast_api_command = f"uvicorn vmagent.rest.api:app --port {rest_config.port}"
    healthcheck_url = f"http://localhost:{rest_config.port}{constants.HEALTHCHECK_ENDPOINT}"

    redis_daemon = conclib.start_redis(config=conclib_config)
    api_daemon_thread = conclib.start_api(
        fast_api_command=fast_api_command,
        healthcheck_url=healthcheck_url,
        startup_healthcheck_timeout=rest_config.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=rest_config.startup_healthcheck_poll_interval,
    )

    conclib.start_proxy(config=conclib_config)

    try:
        while True:
            # Wait until something fails or the user kills the process
            time.sleep(100)
        pass
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
