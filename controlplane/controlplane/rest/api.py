import datetime
from typing import Optional, Annotated
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI, Query, Depends
from controlplane.datastore.types.metrics.generated.cpu import (
    CpuMeasurement,
)
from controlplane.datastore.types.metrics.generated.disk_iops import (
    DiskIopsMeasurement,
)
from controlplane.datastore.types.metrics.generated.disk_usage import (
    DiskUsageMeasurement,
)
from controlplane.datastore.types.metrics.generated.disk_throughput import (
    DiskThroughputMeasurement,
)
from controlplane.datastore.types.metrics.generated.gpu_memory import (
    GpuMemoryMeasurement,
)
from controlplane.datastore.types.metrics.generated.gpu_utilization import (
    GpuUtilizationMeasurement,
)
from controlplane.datastore.types.metrics.generated.memory import (
    MemoryMeasurement,
)
from controlplane.datastore.types.metrics.generated.network_throughput import (
    NetworkThroughputMeasurement,
)
from controlplane.datastore.types.metrics.generated.nvidia_smi import (
    NvidiaSmiMeasurement,
)

from controlplane.datastore.types.machine_info import (
    MachineRegistrationInfo,
    MachineInfo,
)
from common import constants
from controlplane.datastore.client import (
    DatastoreClient,
    MachineRegistrationConflictError,
)
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


@app.post(constants.CONTROL_PLANE_MACHINE_REGISTRATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def register_machine(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_id: str,
    registration_info: MachineRegistrationInfo,
) -> OkResponse:
    """Register a machine"""
    if machine_id in constants.RESERVED_MACHINE_NAMES:
        raise ValueError(
            f"machine_id cannot be '{machine_id}' - these are reserved names: {constants.RESERVED_MACHINE_NAMES}"
        )
    try:
        datastore_client.add_or_update_machine_info(
            machine_id=machine_id, registration_info=registration_info
        )
    except MachineRegistrationConflictError as err:
        err_msg = (
            f"{err}\nThis may be caused by trying to run a new machine with the same machine ID ({machine_id}) "
            f"as an existing machine. If you can see that another machine with this name is active, "
            "pick a different name. If this is intentional (e.g. you shut down one machine,"
            "booted up a new one and want it to have the same name), you can immediately "
            "remove the old machine from the DB (see API docs until the CLI supports it). "
        )
        raise MachineRegistrationConflictError(err_msg)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_MACHINE_HEARTBEAT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def report_machine_heartbeat(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_id: str,
) -> OkResponse:
    """Report a heartbeat for a machine"""
    datastore_client.update_machine_info_heartbeat_ts(machine_id=machine_id)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_MACHINE_DEATH_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def report_machine_death(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_id: str,
) -> OkResponse:
    """
    Report that a machine is dead, so that it is removed immediately.

    This can be useful when you need the live list to update faster than the timeout.
    """
    datastore_client.delete_machine_info(machine_id=machine_id)
    return OkResponse()


@app.get(constants.CONTROL_PLANE_GET_LIVE_MACHINES_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_live_machines(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> list[MachineInfo]:
    """Return a list of the active machines"""
    live_machines = datastore_client.get_live_machines(
        liveness_threshold_secs=constants.MACHINE_NO_HEARTBEAT_LIMBO_SECS
    )
    return live_machines


@app.get(constants.CONTROL_PLANE_GET_MACHINE_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_machine(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_id: str,
) -> MachineInfo:
    """Return"""
    live_machines = datastore_client.get_machines(machine_ids=[machine_id])
    if len(live_machines) == 0:
        raise ValueError(f"Machine {machine_id} not found")  # TODO: Better error type?
    return live_machines[0]


# BEGIN GENERATED CODE


@app.get(constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_cpu_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, CpuMeasurement]:
    """
    Get cpu metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of CpuMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_cpu_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_cpu_measurement() for result in results[machine_id]
        ]

    return final


@app.get(f"{constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_cpu_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, CpuMeasurement]:
    """Get the most recent cpu measurements for each machine"""
    results = datastore_client.get_latest_cpu_measurements(machine_ids=machine_ids)
    return {result.machine_id: result.to_cpu_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_cpu_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: CpuMeasurement,
) -> OkResponse:
    """Put a cpu metric measurement into the datastore"""
    datastore_client.add_cpu_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_iops_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, DiskIopsMeasurement]:
    """
    Get disk_iops metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of DiskIopsMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_disk_iops_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_disk_iops_measurement() for result in results[machine_id]
        ]

    return final


@app.get(f"{constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_disk_iops_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, DiskIopsMeasurement]:
    """Get the most recent disk_iops measurements for each machine"""
    results = datastore_client.get_latest_disk_iops_measurements(
        machine_ids=machine_ids
    )
    return {result.machine_id: result.to_disk_iops_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_iops_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskIopsMeasurement,
) -> OkResponse:
    """Put a disk_iops metric measurement into the datastore"""
    datastore_client.add_disk_iops_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_usage_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, DiskUsageMeasurement]:
    """
    Get disk_usage metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of DiskUsageMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_disk_usage_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_disk_usage_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_disk_usage_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, DiskUsageMeasurement]:
    """Get the most recent disk_usage measurements for each machine"""
    results = datastore_client.get_latest_disk_usage_measurements(
        machine_ids=machine_ids
    )
    return {result.machine_id: result.to_disk_usage_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_usage_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskUsageMeasurement,
) -> OkResponse:
    """Put a disk_usage metric measurement into the datastore"""
    datastore_client.add_disk_usage_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, DiskThroughputMeasurement]:
    """
    Get disk_throughput metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of DiskThroughputMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_disk_throughput_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_disk_throughput_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_disk_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, DiskThroughputMeasurement]:
    """Get the most recent disk_throughput measurements for each machine"""
    results = datastore_client.get_latest_disk_throughput_measurements(
        machine_ids=machine_ids
    )
    return {
        result.machine_id: result.to_disk_throughput_measurement() for result in results
    }


@app.post(constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_throughput_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskThroughputMeasurement,
) -> OkResponse:
    """Put a disk_throughput metric measurement into the datastore"""
    datastore_client.add_disk_throughput_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_gpu_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, GpuMemoryMeasurement]:
    """
    Get gpu_memory metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of GpuMemoryMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_gpu_memory_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_gpu_memory_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_gpu_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, GpuMemoryMeasurement]:
    """Get the most recent gpu_memory measurements for each machine"""
    results = datastore_client.get_latest_gpu_memory_measurements(
        machine_ids=machine_ids
    )
    return {result.machine_id: result.to_gpu_memory_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_gpu_memory_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: GpuMemoryMeasurement,
) -> OkResponse:
    """Put a gpu_memory metric measurement into the datastore"""
    datastore_client.add_gpu_memory_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_gpu_utilization_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, GpuUtilizationMeasurement]:
    """
    Get gpu_utilization metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of GpuUtilizationMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_gpu_utilization_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_gpu_utilization_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_gpu_utilization_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, GpuUtilizationMeasurement]:
    """Get the most recent gpu_utilization measurements for each machine"""
    results = datastore_client.get_latest_gpu_utilization_measurements(
        machine_ids=machine_ids
    )
    return {
        result.machine_id: result.to_gpu_utilization_measurement() for result in results
    }


@app.post(constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_gpu_utilization_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: GpuUtilizationMeasurement,
) -> OkResponse:
    """Put a gpu_utilization metric measurement into the datastore"""
    datastore_client.add_gpu_utilization_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, MemoryMeasurement]:
    """
    Get memory metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of MemoryMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_memory_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_memory_measurement() for result in results[machine_id]
        ]

    return final


@app.get(f"{constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, MemoryMeasurement]:
    """Get the most recent memory measurements for each machine"""
    results = datastore_client.get_latest_memory_measurements(machine_ids=machine_ids)
    return {result.machine_id: result.to_memory_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_memory_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: MemoryMeasurement,
) -> OkResponse:
    """Put a memory metric measurement into the datastore"""
    datastore_client.add_memory_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_network_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, NetworkThroughputMeasurement]:
    """
    Get network_throughput metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of NetworkThroughputMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_network_throughput_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_network_throughput_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT}/latest",
    tags=[MAIN_TAG],
)
@auth(datastore_client)
def get_latest_network_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, NetworkThroughputMeasurement]:
    """Get the most recent network_throughput measurements for each machine"""
    results = datastore_client.get_latest_network_throughput_measurements(
        machine_ids=machine_ids
    )
    return {
        result.machine_id: result.to_network_throughput_measurement()
        for result in results
    }


@app.post(constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_network_throughput_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: NetworkThroughputMeasurement,
) -> OkResponse:
    """Put a network_throughput metric measurement into the datastore"""
    datastore_client.add_network_throughput_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_nvidia_smi_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> dict[str, NvidiaSmiMeasurement]:
    """
    Get nvidia_smi metrics for certain machines between from_ts to to_ts, inclusive.
    :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: Dict of NvidiaSmiMeasurement objects with machine_id as the key.
    """
    results = datastore_client.get_nvidia_smi_measurements(
        machine_ids=machine_ids, start_ts=from_ts, end_ts=to_ts
    )
    final = {}
    for machine_id in results.keys():
        final[machine_id] = [
            result.to_nvidia_smi_measurement() for result in results[machine_id]
        ]

    return final


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_nvidia_smi_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    machine_ids: Annotated[list[str], Query()],
) -> dict[str, NvidiaSmiMeasurement]:
    """Get the most recent nvidia_smi measurements for each machine"""
    results = datastore_client.get_latest_nvidia_smi_measurements(
        machine_ids=machine_ids
    )
    return {result.machine_id: result.to_nvidia_smi_measurement() for result in results}


@app.post(constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_nvidia_smi_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: NvidiaSmiMeasurement,
) -> OkResponse:
    """Put a nvidia_smi metric measurement into the datastore"""
    datastore_client.add_nvidia_smi_measurement(
        machine_id=measurement.machine_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


# END GENERATED CODE


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
