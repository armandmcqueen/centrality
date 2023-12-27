import os
import subprocess
import time
import conclib
import pykka
import typer

from controlplane.rest.config import ControlPlaneRestConfig
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from controlplane.actorsystem import ControlPlaneActorSystem
from common import constants


app = typer.Typer()


@app.command()
def launch(postgres_host: str = "localhost"):
    """
    Launch the Control Plane FastAPI server.

    When we add an actor system, this is where we'll launch it.
    """
    print("📝 Using default configs")
    conclib_config = conclib.DefaultConfig()
    rest_config = ControlPlaneRestConfig()
    datastore_config = DatastoreConfig(config_overrides=dict(host=postgres_host))
    rest_config.save_to_envvar()
    datastore_config.save_to_envvar()

    print("🌰 Setting up DB")
    datastore_client = DatastoreClient(config=datastore_config)
    start_time = time.time()
    while True:
        if time.time() - start_time > 120:
            raise RuntimeError("Timed out waiting for DB to start")
        try:
            datastore_client.setup_db()  # Runs DDL. TODO: Handle proper migrations?
            break
        except Exception as e:
            print(e)
            print("Waiting for DB to start...")
            time.sleep(1)
            continue
    print("✓ DB setup")

    print("🚀 Launching Control Plane actor system")
    # Start conclib bridge
    redis_daemon = conclib.start_redis(config=conclib_config)
    conclib.start_proxy(config=conclib_config)
    _ = ControlPlaneActorSystem(datastore_config=datastore_config).start()
    print("✓ Actor system started")

    print("🚀 Launching Control Plane API")
    api_thread = conclib.start_api(
        fast_api_command=f"uvicorn controlplane.rest.api:app "
        f"--workers {os.cpu_count() * 2} "
        f"--port {rest_config.port} "
        f"--host 0.0.0.0",
        healthcheck_url=f"http://localhost:{rest_config.port}{constants.HEALTHCHECK_ENDPOINT}",
        startup_healthcheck_timeout=rest_config.startup_healthcheck_timeout,
        startup_healthcheck_poll_interval=rest_config.startup_healthcheck_poll_interval,
    )
    print("✓ API started")

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
        pykka.ActorRegistry.stop_all()
        redis_daemon.shutdown()
        print("👋 Goodbye")


@app.command()
def openapi():
    rest_config = ControlPlaneRestConfig()
    datastore_config = DatastoreConfig()
    rest_config.save_to_envvar()
    datastore_config.save_to_envvar()

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
