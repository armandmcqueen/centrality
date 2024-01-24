# Run python code in a sandboxed docker container


import docker
from rich import print
import sys

CONTAINER_IMAGE = "armandmcqueen/centrality-dev:latest"


def write_tmp_and_entrypoint_files(code, install_cmd=":"):
    # Copy the code to run.py in the container
    tmp_file_host = open("/tmp/tmp.py", "w+")
    tmp_file_host.write(code)
    tmp_file_host.close()

    # TODO: Automatically make this executable?
    entrypoint_tmp_file_host = open("/tmp/entrypoint.sh", "w+")
    entrypoint_tmp_file_host.write(
        f"#!/bin/bash\n{install_cmd}\npython3.11 /home/runner/tmp.py"
    )
    entrypoint_tmp_file_host.close()


def run_code():
    client = docker.from_env()
    # Start the container
    container = client.containers.run(
        CONTAINER_IMAGE,
        command="/home/runner/entrypoint.sh",
        # command="sleep infinity",
        detach=True,
        tty=True,
        volumes={
            "/tmp/tmp.py": {"bind": "/home/runner/tmp.py", "mode": "rw"},
            "/tmp/entrypoint.sh": {"bind": "/home/runner/entrypoint.sh", "mode": "rw"},
        },
    )

    print("[green]Output of script")
    # Stream the output
    try:
        for line in container.logs(stream=True):
            # Decode the binary data to a string
            sys.stdout.write(line.decode("utf-8"))
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

    # Wait for the container to finish
    container.wait()
    # while container.status != "exited":
    #     time.sleep(0.1)
    #     container.reload()
    #     print("[white]Container status: " + container.status)

    # Get the output
    # output = container.logs()
    # print(output.decode("utf-8"))
    # Remove the container
    # container.remove()


if __name__ == "__main__":
    run_code("print('Hello World')")
