# Run python code in a sandboxed docker container

import docker
from rich import print
import sys
import os

TMP_FILE_PATH_HOST = "/tmp/run.py"
TMP_FILE_PATH_CONTAINER = "/home/runner/run.py"
ENTRYPOINT_FILE_PATH_HOST = "/tmp/entrypoint.sh"
ENTRYPOINT_FILE_PATH_CONTAINER = "/home/runner/entrypoint.sh"

# TODO: This container needs to be built and pushed to dockerhub regularly if we want to rely on it.
CONTAINER_IMAGE = "armandmcqueen/centrality-dev:latest"


def write_files(code, install_cmd=":"):
    """Write code and entrypoint to locations on the host that will be mounted into the container."""

    with open(TMP_FILE_PATH_HOST, "w+") as tmp_file_host:
        tmp_file_host.write(code)

    with open(ENTRYPOINT_FILE_PATH_HOST, "w+") as entrypoint_tmp_file_host:
        entrypoint_tmp_file_host.write(
            f"#!/bin/bash\n{install_cmd}\npython3.11 {TMP_FILE_PATH_CONTAINER}"
        )

    # Make the entrypoint executable
    os.chmod(ENTRYPOINT_FILE_PATH_HOST, 0o777)


def run_code():
    """Run the code in the container and stream the output. Should be called after write_files."""
    client = docker.from_env()
    container = client.containers.run(
        CONTAINER_IMAGE,
        command=ENTRYPOINT_FILE_PATH_CONTAINER,
        detach=True,
        tty=True,
        volumes={
            TMP_FILE_PATH_HOST: {"bind": TMP_FILE_PATH_CONTAINER, "mode": "rw"},
            ENTRYPOINT_FILE_PATH_HOST: {
                "bind": ENTRYPOINT_FILE_PATH_CONTAINER,
                "mode": "rw",
            },
        },
    )

    print("[green]Output of script")
    # Stream the output
    buffer = b""
    for chunk in container.logs(stream=True):
        buffer += chunk
        try:
            sys.stdout.write(buffer.decode("utf-8"))
            sys.stdout.flush()
            buffer = b""
        except UnicodeDecodeError:
            continue

    # Wait for the container to finish
    container.wait()
    container.remove()
