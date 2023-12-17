from types import TracebackType
from typing import Optional

import psutil
import pykka
import datetime
import conclib
from common import constants
from common.types.vmmetrics import CpuMeasurement
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk, ControlPlaneSdkConfig
from vmagent.config import VmAgentConfig


class CollectCpuMetrics(conclib.ActorMessage):
    pass


class CpuMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR
    TICKS = {
        CollectCpuMetrics: constants.VM_AGENT_METRIC_CPU_INTERVAL_SECS,
    }

    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk
        super().__init__()

    def collect_cpu_metric(self) -> None:
        cpu_percents = psutil.cpu_percent(percpu=True)
        measurement = CpuMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.datetime.utcnow(),
            cpu_percents=cpu_percents,
        )
        self.control_plane_sdk.write_cpu_metric(measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, CollectCpuMetrics):
            self.collect_cpu_metric()
        else:
            raise conclib.errors.UnexpectedMessageError(message)

