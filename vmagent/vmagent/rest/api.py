import datetime
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI
from common import constants
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig
from controlplane.rest.config import ControlPlaneRestConfig


from pydantic import BaseModel


class OkResponse(BaseModel):
    status: str = "ok"


app = FastAPI(
    title="centrality-vmagent",
    version="0.0.1",
)


# Load config values from environment variables and setup connect to datastore
rest_config = ControlPlaneRestConfig.from_envvar()
datastore_config = DatastoreConfig.from_envvar()
datastore_client = DatastoreClient(config=datastore_config)


@app.get(constants.HEALTHCHECK_ENDPOINT)
def get_healthcheck():
    """ Basic healthcheck """
    return OkResponse()


def generate_openapi_json():
    """ Generate the OpenAPI JSON file and print it to stdout. (__main__ calls this) """
    openapi_schema = app.openapi()
    # Write to stdout
    print(json.dumps(openapi_schema, indent=2))


# To improve the naming of auto-generated API clients, we use the route names
# as the operation IDs. Copied from docs:
# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)


if __name__ == '__main__':
    generate_openapi_json()

