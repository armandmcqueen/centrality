import datetime
from typing import Optional, Annotated

from fastapi import FastAPI, Query, Depends
from common.types.vmmetrics import CpuMeasurement
from controlplane import constants
from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DatastoreConfig
from controlplane.rest.config import ControlPlaneRestConfig
from controlplane.rest.auth import auth

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pydantic import BaseModel


class OkResponse(BaseModel):
    status: str = "ok"


app = FastAPI()

rest_config = ControlPlaneRestConfig.from_envvar()
datastore_config = DatastoreConfig.from_envvar()

datastore_client = DatastoreClient(config=datastore_config)


security = HTTPBearer()


@app.get(constants.HEALTHCHECK_ENDPOINT)
def get_healthcheck():
    return OkResponse()


@app.get(constants.AUTH_HEALTHCHECK_ENDPOINT)
@auth(datastore_client)
def get_auth_healthcheck(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
) -> OkResponse:
    return OkResponse()


@app.get(constants.CPU_METRIC_ENDPOINT)
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


@app.post(constants.CPU_METRIC_ENDPOINT)
@auth(datastore_client)
def put_cpu_metric(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],  # noqa
        measurement: CpuMeasurement
) -> OkResponse:
    datastore_client.add_cpu_measurement(
        vm_id=measurement.vm_id,
        cpu_percents=measurement.cpu_percents,
        ts=measurement.ts)
    return OkResponse()



