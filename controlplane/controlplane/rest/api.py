from fastapi import FastAPI
from controlplane import constants
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig
from controlplane.rest.config import ControlPlaneRestConfig

app = FastAPI()

rest_config = ControlPlaneRestConfig.from_envvar()
datastore_config = DatastoreConfig.from_envvar()

datastore_client = DatastoreClient(config=datastore_config)


@app.get(constants.HEALTHCHECK_ENDPOINT)
def get_healthcheck():
    return {"status": "ok"}
