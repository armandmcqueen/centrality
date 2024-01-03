import datetime
from typing import Optional, Annotated
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI, Query, Depends
from common.types.vmmetrics import CpuMeasurement
from controlplane.datastore.types.vmliveness import VmRegistration
from common import constants
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig
from controlplane.rest.config import ControlPlaneRestConfig
from controlplane.rest.utils.auth import auth, security
# from controlplane.rest.example.api import router as example_router

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

MAIN_TAG = "data"


class OkResponse(BaseModel):
    status: str = "ok"


class InfoResponse(BaseModel):
    git_commit: str
    git_branch: str
    git_is_dirty: bool
    deploy_time: datetime.datetime


deploy_time = datetime.datetime.now()
app = FastAPI(
    title="centrality-controlplane",
    version="0.0.1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(example_router)


# Load config values from environment variables and setup connect to datastore
rest_config = ControlPlaneRestConfig.from_envvar()
datastore_config = DatastoreConfig.from_envvar()
datastore_client = DatastoreClient(config=datastore_config)


# Add git support if we can - if there is a git executable and a git repo.
try:
    from git import Repo, InvalidGitRepositoryError  # noqa

    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        print(
            f"❗️Not in a git repository, can't get git commit/branch. Error: {e}\nNote: this is a NONFATAL error."
        )
        repo = None
except ImportError as e:
    print(
        f"❗️Failed to import gitpython, can't get git commit/branch. Error: {e}\nNote: this is a NONFATAL error."
    )
    repo = None


@app.get(constants.HEALTHCHECK_ENDPOINT, tags=[MAIN_TAG])
def get_healthcheck() -> OkResponse:
    """Basic healthcheck"""
    return OkResponse()


@app.get(constants.AUTH_HEALTHCHECK_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_auth_healthcheck(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> OkResponse:
    """Basic healthcheck that requires authentication"""
    return OkResponse()


@app.get(constants.INFO_ENDPOINT, tags=[MAIN_TAG])
def get_info() -> InfoResponse:
    """Return basic info about deployment"""
    git_branch = "unknown"
    git_commit = "unknown"
    git_is_dirty = False

    if repo is not None:
        try:
            git_branch = repo.active_branch.name
        except Exception:
            print("❗️Failed to get git branch. NONFATAL error.")

        try:
            git_commit = repo.head.commit.hexsha
        except Exception:
            print("❗️Failed to get git commit. NONFATAL error.")

        try:
            git_is_dirty = repo.is_dirty(untracked_files=True)
        except Exception:
            print("❗️Failed to get git dirty status. NONFATAL error.")

    return InfoResponse(
        git_branch=git_branch,
        git_commit=git_commit,
        git_is_dirty=git_is_dirty,
        deploy_time=deploy_time,
    )


@app.get(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_cpu_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
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
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [
        CpuMeasurement(
            vm_id=result.vm_id, cpu_percents=result.cpu_percents, ts=result.ts
        )
        for result in results
    ]


@app.get(constants.CONTROL_PLANE_LATEST_CPU_METRIC_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_cpu_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[CpuMeasurement]:
    """Get the most recent CPU measurements for each VM"""
    results = datastore_client.get_latest_cpu_measurements(vm_ids=vm_ids)
    return [
        CpuMeasurement(
            vm_id=result.vm_id, cpu_percents=result.cpu_percents, ts=result.ts
        )
        for result in results
    ]


@app.post(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_cpu_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: CpuMeasurement,
) -> OkResponse:
    """Put a cpu metric measurement into the datastore"""
    datastore_client.add_cpu_measurement(
        vm_id=measurement.vm_id,
        cpu_percents=measurement.cpu_percents,
        ts=measurement.ts,
    )
    return OkResponse()


@app.post(constants.CONTROL_PLANE_VM_REGISTRATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def register_vm(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    registration_info: VmRegistration,
) -> OkResponse:
    """Register a VM"""
    datastore_client.register_vm(registration_info=registration_info)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_VM_HEARTBEAT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def report_vm_heartbeat(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_id: str,
) -> OkResponse:
    """Report a heartbeat for a VM"""
    datastore_client.report_heartbeat(vm_id=vm_id)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_VM_DEATH_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def report_vm_death(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_id: str,
) -> OkResponse:
    """
    Report that a VM is dead, so that it is removed immediately.

    This can be useful when you need the live list to update faster than the timeout.
    """
    datastore_client.report_vm_death(vm_id=vm_id)
    return OkResponse()


@app.get(constants.CONTROL_PLANE_LIVE_VM_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def list_live_vms(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> list[str]:
    """Return a list of the active VMs"""
    # TODO: Convert to return machine info
    live_vms = datastore_client.get_live_vms(
        liveness_threshold_secs=constants.VM_HEARTBEAT_TIMEOUT_SECS
    )
    return live_vms


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
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)


if __name__ == "__main__":
    generate_openapi_json()
