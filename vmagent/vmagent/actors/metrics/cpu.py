import datetime
import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.faketrics import FakeMetricGenerator
from vmagent.actors.metrics.samplers.cpu import CpuSampler
from centrality_controlplane_sdk import DataApi, CpuMeasurement


class SendCpuMetrics(conclib.ActorMessage):
    pass


class CpuMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendCpuMetrics: constants.VM_AGENT_METRIC_CPU_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,  # TODO: Only need vm_id
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk
        self.config = self.vm_agent_config.metrics.cpu

        self.sampler = CpuSampler()
        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_cpu_metric(self) -> None:
        if self.config.use_fake:
            cpu_percents = self.fake_metric_generator.sample()
        else:
            cpu_percents = self.sampler.sample()

        # print(f"📡 {self.__class__.__name__} - sending metrics: {cpu_percents}")

        measurement = CpuMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.datetime.now(datetime.timezone.utc),
            cpu_percents=cpu_percents,
        )
        self.control_plane_sdk.put_cpu_metric(cpu_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendCpuMetrics):
            try:
                self.send_cpu_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
