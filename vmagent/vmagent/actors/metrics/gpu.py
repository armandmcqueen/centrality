from types import TracebackType
from typing import Optional

import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.gpu import GpuSampler
from actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi


class PynvmlNotAvailableError(Exception):
    pass


class SendGpuMetrics(conclib.ActorMessage):
    pass


class GpuMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_GPU_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendGpuMetrics: constants.VM_AGENT_METRIC_GPU_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_id: VmAgentConfig,
        gpu_util_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.config_util = self.vm_agent_config.metrics.gpu_util
        self.config_mem = self.vm_agent_config.metrics.gpu_mem
        self.control_plane_sdk = control_plane_sdk

        if self.config_util.use_fake and self.config_mem.use_fake:
            if self.config_util.fake.num_vals != self.config_mem.fake.num_vals:
                raise ValueError(
                    "GpuMetricConfig.fake.num_vals must be the same for both gpu_util and gpu_mem!"
                )

        self.sampler = GpuSampler()
        self.fake_metric_generator_util = FakeMetricGenerator(self.config_util.fake)
        self.fake_metric_generator_mem = FakeMetricGenerator(self.config_mem.fake)
        super().__init__()

    def send_gpu_metric(self) -> None:
        # If we aren't faking all the data, check if pynvml is available and exception if not
        utils = None
        mem = None
        if not (self.config_util.use_fake and self.config_mem.use_fake):
            if not self.sampler.pynvml_active:
                raise PynvmlNotAvailableError("pynvml is not available on this system")
            utils, mem = self.sampler.sample()

        if self.config_util.use_fake:
            utils = self.fake_metric_generator_util.sample()
        if self.config_mem.use_fake:
            used_mems = self.fake_metric_generator_mem.sample()
            mem = [(used_mem, self.config_mem.fake.max_val) for used_mem in used_mems]

        print(f"📡 {self.__class__.__name__} - sending metrics: {utils, mem}")

        pass
        # measurement = CpuMeasurement(
        #     vm_id=self.vm_agent_config.vm_id,
        #     ts=datetime.datetime.now(datetime.timezone.utc),
        #     cpu_percents=cpu_percents,
        # )
        # self.control_plane_sdk.put_cpu_metric(cpu_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendGpuMetrics):
            try:
                self.send_gpu_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)

    def on_stop(self) -> None:
        self.sampler.shutdown()
        super().on_stop()

    def on_failure(
        self,
        exception_type: Optional[type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.sampler.shutdown()
        super().on_failure(exception_type, exception_value, traceback)
