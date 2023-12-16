import subprocess
import time
import conclib
import typer

from controlplane.rest.config import ControlPlaneRestConfig
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from common import constants


app = typer.Typer()


def get_default_configs() -> tuple[ControlPlaneRestConfig, DatastoreConfig]:
    rest_config = ControlPlaneRestConfig()
    datastore_config = DatastoreConfig()
    return rest_config, datastore_config


@app.command()
def launch(postgres_host: str = "localhost"):
    """
    Launch the Control Plane FastAPI server.

    When we add an actor system, this is where we'll launch it.
    """
    # TODO: Allow for non-default configs
    print("📝 Using default configs")
    rest_config, datastore_config = get_default_configs()
    datastore_config.host = postgres_host  # TODO: Remove this hacky approach to configs
    rest_config.save_as_envvar()
    datastore_config.save_as_envvar()
    print("🚀 Launching Control Plane API")

    launch_command = f"uvicorn controlplane.rest.api:app --port {rest_config.port} --host 0.0.0.0"
    healthcheck_url = f"http://localhost:{rest_config.port}{constants.HEALTHCHECK_ENDPOINT}"
    api_thread = conclib.start_api(
        fast_api_command=launch_command,
        healthcheck_url=healthcheck_url,
        startup_healthcheck_timeout=rest_config.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=rest_config.startup_healthcheck_poll_interval,
    )

    try:
        while True:
            # Wait until something fails or the user kills the process
            time.sleep(100)
    except KeyboardInterrupt:
        print()  # Print a newline to make the output look nicer after ^C
        print("🛑 KeyboardInterrupt encountered, shutting down REST API")
    except Exception as e:
        print(e)
        print(f"❗️Control Plane API shutting down due to {type(e)} exception")
    finally:
        api_thread.shutdown()
        print("👋 Goodbye")


@app.command()
def openapi():
    rest_config, datastore_config = get_default_configs()
    rest_config.save_as_envvar()
    datastore_config.save_as_envvar()

    out = subprocess.check_output("python -m controlplane.rest.api", shell=True)
    print(out.decode("utf-8"))


@app.command()
def reset_datastore():
    """
    Reset the datastore to a clean state.

    This will delete all data in the datastore and reset the schema.
    """
    datastore_config = DatastoreConfig()
    datastore_client = DatastoreClient(config=datastore_config)
    datastore_client.reset_db()


@app.command()
def hello():
    print("Hello, world, this is the Control Plane CLI!")


if __name__ == "__main__":
    app()
