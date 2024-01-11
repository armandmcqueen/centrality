import datetime
from typing import Optional, Annotated
import json

from fastapi.routing import APIRoute
from fastapi import FastAPI, Query, Depends
from controlplane.datastore.types.vmmetrics.generated.cpu import (
    CpuMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.disk_iops import (
    DiskIopsMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.disk_usage import (
    DiskUsageMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.disk_throughput import (
    DiskThroughputMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.gpu_memory import (
    GpuMemoryMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.gpu_utilization import (
    GpuUtilizationMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.memory import (
    MemoryMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.network_throughput import (
    NetworkThroughputMeasurement,
)
from controlplane.datastore.types.vmmetrics.generated.nvidia_smi import (
    NvidiaSmiMeasurement,
)

from controlplane.datastore.types.vmliveness import VmRegistrationInfo
from common import constants
from controlplane.datastore.client import DatastoreClient, VmRegistrationConflictError
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


@app.post(constants.CONTROL_PLANE_VM_REGISTRATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def register_vm(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_id: str,
    registration_info: VmRegistrationInfo,
) -> OkResponse:
    """Register a VM"""
    try:
        datastore_client.add_or_update_vm_info(
            vm_id=vm_id, registration_info=registration_info
        )
    except VmRegistrationConflictError as err:
        err_msg = (
            f"{err}\nThis may be caused by trying to run a new VM with the same VM ID ({vm_id}) "
            f"as an existing VM. If you can see that another VM with this name is active, "
            "pick a different name. If this is intentional (e.g. you shut down one machine,"
            "booted up a new one and want it to have the same name), you can immediately "
            "remove the old VM from the DB (see API docs until the CLI supports it). "
        )
        raise VmRegistrationConflictError(err_msg)
    return OkResponse()


@app.post(constants.CONTROL_PLANE_VM_HEARTBEAT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def report_vm_heartbeat(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_id: str,
) -> OkResponse:
    """Report a heartbeat for a VM"""
    datastore_client.update_vm_info_heartbeat_ts(vm_id=vm_id)
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
    datastore_client.delete_vm_info(vm_id=vm_id)
    return OkResponse()


@app.get(constants.CONTROL_PLANE_LIVE_VM_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def list_live_vms(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> list[str]:
    """Return a list of the active VMs"""
    # TODO: Convert to return machine info
    live_vms = datastore_client.get_live_vms(
        liveness_threshold_secs=constants.VM_NO_HEARTBEAT_LIMBO_SECS
    )
    return live_vms


# BEGIN GENERATED CODE


@app.get(constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT, tags=[MAIN_TAG])
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
    return [result.to_cpu_measurement() for result in results]


@app.get(f"{constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_cpu_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[CpuMeasurement]:
    """Get the most recent cpu measurements for each VM"""
    results = datastore_client.get_latest_cpu_measurements(vm_ids=vm_ids)
    return [result.to_cpu_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_CPU_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_cpu_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: CpuMeasurement,
) -> OkResponse:
    """Put a cpu metric measurement into the datastore"""
    datastore_client.add_cpu_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_iops_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[DiskIopsMeasurement]:
    """
    Get disk_iops metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of DiskIopsMeasurement objects
    """
    results = datastore_client.get_disk_iops_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_disk_iops_measurement() for result in results]


@app.get(f"{constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_disk_iops_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[DiskIopsMeasurement]:
    """Get the most recent disk_iops measurements for each VM"""
    results = datastore_client.get_latest_disk_iops_measurements(vm_ids=vm_ids)
    return [result.to_disk_iops_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_iops_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskIopsMeasurement,
) -> OkResponse:
    """Put a disk_iops metric measurement into the datastore"""
    datastore_client.add_disk_iops_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_usage_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[DiskUsageMeasurement]:
    """
    Get disk_usage metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of DiskUsageMeasurement objects
    """
    results = datastore_client.get_disk_usage_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_disk_usage_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_disk_usage_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[DiskUsageMeasurement]:
    """Get the most recent disk_usage measurements for each VM"""
    results = datastore_client.get_latest_disk_usage_measurements(vm_ids=vm_ids)
    return [result.to_disk_usage_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_usage_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskUsageMeasurement,
) -> OkResponse:
    """Put a disk_usage metric measurement into the datastore"""
    datastore_client.add_disk_usage_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_disk_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[DiskThroughputMeasurement]:
    """
    Get disk_throughput metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of DiskThroughputMeasurement objects
    """
    results = datastore_client.get_disk_throughput_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_disk_throughput_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_disk_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[DiskThroughputMeasurement]:
    """Get the most recent disk_throughput measurements for each VM"""
    results = datastore_client.get_latest_disk_throughput_measurements(vm_ids=vm_ids)
    return [result.to_disk_throughput_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_disk_throughput_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: DiskThroughputMeasurement,
) -> OkResponse:
    """Put a disk_throughput metric measurement into the datastore"""
    datastore_client.add_disk_throughput_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_gpu_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[GpuMemoryMeasurement]:
    """
    Get gpu_memory metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of GpuMemoryMeasurement objects
    """
    results = datastore_client.get_gpu_memory_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_gpu_memory_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_gpu_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[GpuMemoryMeasurement]:
    """Get the most recent gpu_memory measurements for each VM"""
    results = datastore_client.get_latest_gpu_memory_measurements(vm_ids=vm_ids)
    return [result.to_gpu_memory_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_gpu_memory_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: GpuMemoryMeasurement,
) -> OkResponse:
    """Put a gpu_memory metric measurement into the datastore"""
    datastore_client.add_gpu_memory_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_gpu_utilization_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[GpuUtilizationMeasurement]:
    """
    Get gpu_utilization metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of GpuUtilizationMeasurement objects
    """
    results = datastore_client.get_gpu_utilization_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_gpu_utilization_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_gpu_utilization_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[GpuUtilizationMeasurement]:
    """Get the most recent gpu_utilization measurements for each VM"""
    results = datastore_client.get_latest_gpu_utilization_measurements(vm_ids=vm_ids)
    return [result.to_gpu_utilization_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_gpu_utilization_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: GpuUtilizationMeasurement,
) -> OkResponse:
    """Put a gpu_utilization metric measurement into the datastore"""
    datastore_client.add_gpu_utilization_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[MemoryMeasurement]:
    """
    Get memory metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of MemoryMeasurement objects
    """
    results = datastore_client.get_memory_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_memory_measurement() for result in results]


@app.get(f"{constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT}/latest", tags=[MAIN_TAG])
@auth(datastore_client)
def get_latest_memory_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[MemoryMeasurement]:
    """Get the most recent memory measurements for each VM"""
    results = datastore_client.get_latest_memory_measurements(vm_ids=vm_ids)
    return [result.to_memory_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_MEMORY_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_memory_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: MemoryMeasurement,
) -> OkResponse:
    """Put a memory metric measurement into the datastore"""
    datastore_client.add_memory_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_network_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[NetworkThroughputMeasurement]:
    """
    Get network_throughput metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of NetworkThroughputMeasurement objects
    """
    results = datastore_client.get_network_throughput_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_network_throughput_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT}/latest",
    tags=[MAIN_TAG],
)
@auth(datastore_client)
def get_latest_network_throughput_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[NetworkThroughputMeasurement]:
    """Get the most recent network_throughput measurements for each VM"""
    results = datastore_client.get_latest_network_throughput_measurements(vm_ids=vm_ids)
    return [result.to_network_throughput_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_network_throughput_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: NetworkThroughputMeasurement,
) -> OkResponse:
    """Put a network_throughput metric measurement into the datastore"""
    datastore_client.add_network_throughput_measurement(
        vm_id=measurement.vm_id,
        metrics=measurement.to_metrics(),
        ts=measurement.ts,
    )
    return OkResponse()


@app.get(constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def get_nvidia_smi_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
    from_ts: Optional[datetime.datetime] = None,
    to_ts: Optional[datetime.datetime] = None,
) -> list[NvidiaSmiMeasurement]:
    """
    Get nvidia_smi metrics for certain VMs between from_ts to to_ts, inclusive.
    :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error).
    :param from_ts: Start time filter, inclusive. Optional.
    :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an
                  error, but the results will be empty.
    :return: List of NvidiaSmiMeasurement objects
    """
    results = datastore_client.get_nvidia_smi_measurements(
        vm_ids=vm_ids, start_ts=from_ts, end_ts=to_ts
    )
    return [result.to_nvidia_smi_measurement() for result in results]


@app.get(
    f"{constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT}/latest", tags=[MAIN_TAG]
)
@auth(datastore_client)
def get_latest_nvidia_smi_metrics(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    vm_ids: Annotated[list[str], Query()],
) -> list[NvidiaSmiMeasurement]:
    """Get the most recent nvidia_smi measurements for each VM"""
    results = datastore_client.get_latest_nvidia_smi_measurements(vm_ids=vm_ids)
    return [result.to_nvidia_smi_measurement() for result in results]


@app.post(constants.CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT, tags=[MAIN_TAG])
@auth(datastore_client)
def put_nvidia_smi_metric(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
    measurement: NvidiaSmiMeasurement,
) -> OkResponse:
    """Put a nvidia_smi metric measurement into the datastore"""
    datastore_client.add_nvidia_smi_measurement(
        vm_id=measurement.vm_id,
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
