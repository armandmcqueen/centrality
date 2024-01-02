import pytest
from ..utils.utils import PostgresContainer
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
import time
from rich import print


@pytest.fixture(scope="session")
def datastore():
    """
    Start the Postgres container, wait for it to be healthy, and clean up after tests are done.
    """
    with PostgresContainer():
        print("⬆ Postgres container launched")

        config = DatastoreConfig()
        client = DatastoreClient(config)
        print("🕕 Waiting for DB to start...")

        start_time = time.time()
        while True:
            if time.time() - start_time > 120:
                raise RuntimeError("❌ Timed out waiting for DB to start")
            try:
                client.setup_db()
                break
            except Exception as e:
                print(e)
                print("🕕 Waiting for DB to start...")
                time.sleep(1)
                continue
        print("✓ DB setup")

        yield config, client


@pytest.fixture(autouse=True)
def setup_code(datastore: tuple[DatastoreConfig, DatastoreClient]):
    """Make sure that every test starts with a clean DB"""
    config, client = datastore
    client.reset_db()
