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
from vmagent.actors.metrics.faketrics import FakeMetricGenerator


class SendCpuMetrics(conclib.ActorMessage):
    pass


class CpuMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendCpuMetrics: constants.VM_AGENT_METRIC_CPU_INTERVAL_SECS,
    }

    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk

        self.fake_metrics = self.vm_agent_config.metrics.cpu.use_fake
        self.fake_metric_generator: FakeMetricGenerator | None = None
        if self.fake_metrics:
            self.fake_metric_generator = FakeMetricGenerator(self.vm_agent_config.metrics.cpu.fake)
        super().__init__()

    def send_cpu_metric(self) -> None:
        if self.fake_metrics:
            cpu_percents = self.fake_metric_generator.sample()
        else:
            cpu_percents = psutil.cpu_percent(percpu=True)

        measurement = CpuMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.datetime.utcnow(),
            cpu_percents=cpu_percents,
        )
        self.control_plane_sdk.write_cpu_metric(measurement=measurement)


    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendCpuMetrics):
            try:
                # TODO: Readd this once we have leveled logging?
                # print("⬆ CpuMetricCollector - sending cpu metric")
                self.send_cpu_metric()
            except Exception as e:
                # TODO: Be more thoughtful about this
                print(f"🚨 CpuMetricCollector - failed to send cpu metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)

