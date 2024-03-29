import datetime
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI
from common import constants
from machineagent.rest.config import MachineAgentRestConfig


from pydantic import BaseModel


class OkResponse(BaseModel):
    status: str = "ok"


class InfoResponse(BaseModel):
    deploy_time: datetime.datetime


deploy_time = datetime.datetime.now()
app = FastAPI(
    title="centrality-machineagent",
    version="0.0.1",
)


# Load config values from environment variables and setup connect to datastore
rest_config = MachineAgentRestConfig.from_envvar()


@app.get(constants.HEALTHCHECK_ENDPOINT)
def get_healthcheck():
    """Basic healthcheck"""
    return OkResponse()


@app.get(constants.INFO_ENDPOINT)
def get_info():
    """Return basic info about deployment"""
    return InfoResponse(deploy_time=deploy_time)


def generate_openapi_json():
    """Generate the OpenAPI JSON file and print it to stdout. (__main__ calls this)"""
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


if __name__ == "__main__":
    generate_openapi_json()
