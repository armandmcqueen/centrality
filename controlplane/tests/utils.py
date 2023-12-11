import docker
import uuid


def run_postgres_docker():
    pass


def run_postgres_process():
    pass


class PostgresContainer:
    """Class to launch postgres container as a context manager"""

    def __init__(self, name=None):
        unique_id = name if name else str(uuid.uuid4())
        self.name = f"datastore-postgres-{unique_id}"
        self.client = docker.from_env()
        self.container = None

    def __enter__(self):
        try:
            self.container = self.client.containers.run(
                image="postgres:16.1",
                name=self.name,
                ports={"5432": "5432"},
                environment={"POSTGRES_PASSWORD": "postgres"},
                detach=True,
                remove=True,
            )
        except Exception as e:
            print("Failed to launch postgres container")
            try:
                self.container.stop()
            except Exception:
                pass
            raise e

        return self.container

    def __exit__(self, exc_type, exc_value, traceback):
        if self.container:
            self.container.stop()
