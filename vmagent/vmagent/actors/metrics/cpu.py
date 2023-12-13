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


class CpuMetricCollector(conclib.Actor):
    URN = constants.VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR

    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk_config: ControlPlaneSdkConfig,
            control_plane_sdk_token: str,
    ):
        self.control_plane_sdk_config = control_plane_sdk_config
        self.vm_agent_config = vm_agent_config
        self.ticker: Optional[CpuMetricCollectorTicker] = None
        self.control_plane_sdk = ControlPlaneSdk(config=control_plane_sdk_config, token=control_plane_sdk_token)
        super().__init__(
            urn=self.URN,
        )

    def on_start(self) -> None:
        self.ticker = CpuMetricCollectorTicker(self.actor_ref)
        self.ticker.start()

    def on_stop(self) -> None:
        self.ticker.stop()

    def on_failure(
        self,
        exception_type: Optional[type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.ticker.stop()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, CollectCpuMetrics):
            cpu_percents = psutil.cpu_percent(percpu=True)
            measurement = CpuMeasurement(
                vm_id=self.vm_agent_config.vm_id,
                ts=datetime.datetime.utcnow(),
                cpu_percents=cpu_percents,
            )
            self.control_plane_sdk.write_cpu_metric(measurement=measurement)
        else:
            raise conclib.errors.UnexpectedMessageError(message)


class CpuMetricCollectorTicker(conclib.Ticker):
    def __init__(self, cpu_metric_collector: pykka.ActorRef):
        self.cpu_metric_collector = cpu_metric_collector
        super().__init__(
            interval=0.5,
        )

    def execute(self):
        self.cpu_metric_collector.tell(CollectCpuMetrics())
