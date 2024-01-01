import pytest
from ..utils.utils import PostgresContainer
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
import time


@pytest.fixture(scope="session")
def datastore():
    """
    Start the Postgres container, wait for it to be healthy, and clean up after tests are done.
    """
    with PostgresContainer():
        print("Postgres container launched")
        SLEEP_TIME = 5
        print(f"Sleeping for {SLEEP_TIME} seconds to allow postgres to start")
        time.sleep(SLEEP_TIME)
        config = DatastoreConfig()
        client = DatastoreClient(config)
        client.setup_db()
        print("Setup complete")

        yield config, client
