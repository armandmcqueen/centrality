import time
import typer

from controlplane.rest.config import DefaultControlPlaneRestConfig
from controlplane.datastore.config import DefaultDatastoreConfig
from controlplane.rest.apid import RestApiDaemonThread


def launch_api():
    """
    Launch the Control Plane FastAPI server.

    When we add an actor system, this is where we'll launch it.
    """
    # TODO: Allow for non-default configs
    rest_config = DefaultControlPlaneRestConfig()
    rest_config.save_to_envvar()

    datastore_config = DefaultDatastoreConfig()
    datastore_config.save_to_envvar()

    rest_api_daemon_thread = RestApiDaemonThread(config=rest_config)
    rest_api_daemon_thread.start()

    rest_api_daemon_thread.wait_for_healthy()

    while True:
        try:
            # Wait until something fails or the user kills the process
            # TODO: Does the while loop even do anything useful here?
            time.sleep(100)
        except KeyboardInterrupt:
            print()  # Print a newline to make the output look nicer after ^C
            print("🛑 KeyboardInterrupt encountered, shutting down REST API")
            rest_api_daemon_thread.shutdown()
            print("👋 Goodbye")
            return
        except Exception as e:
            print(e)
            print(f"❗️Control Plane API shutting down due to {type(e)} exception")
            rest_api_daemon_thread.shutdown()
            print("👋 Goodbye")
            return


if __name__ == "__main__":
    typer.run(launch_api)
