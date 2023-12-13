import datetime
from typing import Optional, Annotated
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI, Query, Depends
from common.types.vmmetrics import CpuMeasurement
from common import constants
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig
from controlplane.rest.config import ControlPlaneRestConfig
from controlplane.rest.auth import auth

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pydantic import BaseModel


class OkResponse(BaseModel):
    status: str = "ok"


app = FastAPI(
    title="centrality-controlplane",
    version="0.0.1",
)
security = HTTPBearer()


# Load config values from environment variables and setup connect to datastore
rest_config = ControlPlaneRestConfig.from_envvar()
datastore_config = DatastoreConfig.from_envvar()
datastore_client = DatastoreClient(config=datastore_config)


@app.get(constants.HEALTHCHECK_ENDPOINT)
def get_healthcheck():
    """ Basic healthcheck """
    return OkResponse()


@app.get(constants.AUTH_HEALTHCHECK_ENDPOINT)
@auth(datastore_client)
def get_auth_healthcheck(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> OkResponse:
    """ Basic healthcheck that requires authentication """
    return OkResponse()


@app.get(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT)
@auth(datastore_client)
def get_cpu_metric(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
        vm_ids: Annotated[list[str], Query()],
        from_ts: Optional[datetime.datetime] = None,
        to_ts: Optional[datetime.datetime] = None
) -> list[CpuMeasurement]:
    """
    Get cpu metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of CpuMeasurement objects
    """
    results = datastore_client.get_cpu_measurements(
        vm_ids=vm_ids,
        start_ts=from_ts,
        end_ts=to_ts
    )
    return [CpuMeasurement(
        vm_id=result.vm_id,
        cpu_percents=result.cpu_percents,
        ts=result.ts
    ) for result in results]


@app.get(constants.CONTROL_PLANE_LATEST_CPU_METRIC_ENDPOINT)
@auth(datastore_client)
def get_latest_cpu_measurements(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
        vm_ids: Annotated[list[str], Query()],
) -> list[CpuMeasurement]:
    results = datastore_client.get_latest_cpu_measurements(vm_ids=vm_ids)
    return [CpuMeasurement(
        vm_id=result.vm_id,
        cpu_percents=result.cpu_percents,
        ts=result.ts
    ) for result in results]


@app.post(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT)
@auth(datastore_client)
def put_cpu_metric(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
        measurement: CpuMeasurement
) -> OkResponse:
    """ Put a cpu metric measurement into the datastore """
    datastore_client.add_cpu_measurement(
        vm_id=measurement.vm_id,
        cpu_percents=measurement.cpu_percents,
        ts=measurement.ts)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_VM_HEARTBEAT_ENDPOINT)
@auth(datastore_client)
def report_heartbeat(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
        vm_id: str
) -> OkResponse:
    """ Put a cpu metric measurement into the datastore """
    datastore_client.report_heartbeat(vm_id=vm_id)
    return OkResponse()


@app.get(constants.CONTROL_PLANE_VM_LIST_ENDPOINT)
@auth(datastore_client)
def list_vms(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> list[str]:
    """ Return a list of the active VMs """
    live_vms = datastore_client.get_live_vms(liveness_threshold_secs=constants.VM_HEARTBEAT_TIMEOUT_SECS)
    print(live_vms)
    return live_vms


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
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)


if __name__ == '__main__':
    generate_openapi_json()

