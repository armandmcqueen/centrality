import datetime
import requests

from typing import Optional

from common import constants
from common.types.vmmetrics import CpuMeasurement
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig


class Client:
    def __init__(self, config: ControlPlaneSdkConfig, token: str):
        self.token = token
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            # Add other common headers if needed
        }

    def _build_url(self, endpoint: str) -> str:
        scheme = "https" if self.config.https else "http"
        url = f"{scheme}://{self.config.host}:{self.config.port}{endpoint}"
        return url

    def get_healthcheck(self) -> requests.Response:
        url = self._build_url(constants.HEALTHCHECK_ENDPOINT)
        return requests.get(url)

    def get_auth_healthcheck(self) -> requests.Response:
        url = self._build_url(constants.AUTH_HEALTHCHECK_ENDPOINT)
        return requests.get(url, headers=self.headers)

    def write_cpu_metric(self, measurement: CpuMeasurement) -> requests.Response:
        url = self._build_url(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT)
        return requests.post(url, headers=self.headers, data=measurement.model_dump_json())

    def get_cpu_metric(
            self,
            vm_ids: list[str],
            from_ts: Optional[datetime.datetime] = None,
            to_ts: Optional[datetime.datetime] = None,
    ) -> tuple[requests.Response, list[CpuMeasurement]]:
        url = self._build_url(constants.CONTROL_PLANE_CPU_METRIC_ENDPOINT)
        params = dict(
            vm_ids=vm_ids,
        )
        if from_ts is not None:
            params["from_ts"] = from_ts.isoformat()
        if to_ts is not None:
            params["to_ts"] = to_ts.isoformat()
        response = requests.get(url, headers=self.headers, params=params)
        measurements = [CpuMeasurement(**j) for j in response.json()]
        return response, measurements
