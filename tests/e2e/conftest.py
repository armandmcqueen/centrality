# conftest.py
import pytest
import subprocess
from pathlib import Path

compose_file_path = Path(__file__).parent.parent.parent / "compose.yaml"
compose_override_file_path = Path(__file__).parent.parent.parent / "compose-override-mountcode.yaml"
logs_file_path = Path(__file__).parent / "docker_logs.txt"



@pytest.fixture(scope="session")
def docker_compose():
    # Start Docker Compose
    subprocess.run(f"docker compose -f {compose_file_path.absolute()} -f {compose_override_file_path.absolute()} up -d", shell=True, check=True)

    # Yield to allow tests to run
    yield

    # Teardown: Stop Docker Compose and gather logs
    subprocess.run(f"docker compose logs > {logs_file_path}", shell=True, check=True)
    subprocess.run("docker compose down", shell=True, check=True)
