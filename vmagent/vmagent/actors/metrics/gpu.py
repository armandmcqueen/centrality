from types import TracebackType
from typing import Optional

import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.gpu import GpuSampler
from vmagent.actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import (
    DataApi,
    GpuMemoryMeasurement,
    GpuUtilizationMeasurement,
    GpuMemory,
)
from datetime import datetime, timezone


class SendGpuMetrics(conclib.ActorMessage):
    pass


class GpuMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_GPU_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendGpuMetrics: constants.VM_AGENT_METRIC_GPU_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config_util = self.vm_agent_config.metrics.gpu_utilization
        self.config_mem = self.vm_agent_config.metrics.gpu_memory
        self.control_plane_sdk = control_plane_sdk

        if self.config_util.use_fake and self.config_mem.use_fake:
            if self.config_util.fake.num_vals != self.config_mem.fake.num_vals:
                raise ValueError(
                    "fake.num_vals must be the same for both gpuutil and gpumem!"
                )

        self.sampler = GpuSampler()
        self.fake_metric_generator_util = FakeMetricGenerator(self.config_util.fake)
        self.fake_metric_generator_mem = FakeMetricGenerator(self.config_mem.fake)
        super().__init__()

    def send_gpu_metric(self) -> None:
        # If we aren't faking all the data, check if pynvml is available and skip sampling if not
        utils = None
        mem = None
        if not (self.config_util.use_fake and self.config_mem.use_fake):
            if not self.sampler.pynvml_available:
                # TODO: Add trace logging once logging is configured
                # print(
                #     f"🚨 {self.__class__.__name__} - pynvml not available, skipping gpu metric"
                # )
                return
            utils, mem = self.sampler.sample()

        if self.config_util.use_fake:
            utils = self.fake_metric_generator_util.sample()
        if self.config_mem.use_fake:
            used_mems = self.fake_metric_generator_mem.sample()
            mem = [
                GpuMemory(used_mb=used_mem, total_mb=self.config_mem.fake.max_val)
                for used_mem in used_mems
            ]

        # print(f"📡 {self.__class__.__name__} - sending metrics: {utils=}, {mem=}")

        now = datetime.now(timezone.utc)
        memory_measurement = GpuMemoryMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=now,
            memory=mem,
        )
        util_measurement = GpuUtilizationMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=now,
            gpu_percents=utils,
        )
        self.control_plane_sdk.put_gpu_memory_metric(
            gpu_memory_measurement=memory_measurement
        )
        self.control_plane_sdk.put_gpu_utilization_metric(
            gpu_utilization_measurement=util_measurement
        )

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


def test():
    FAKE = True
    import time
    from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig

    config = VmAgentConfig()
    config.metrics.gpu_utilization.use_fake = FAKE
    config.metrics.gpu_memory.use_fake = FAKE
    control_plane_sdk_config = ControlPlaneSdkConfig()
    control_plane_sdk = get_sdk(
        control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    actor = GpuMetricCollector.start(
        vm_agent_config=config, control_plane_sdk=control_plane_sdk
    )
    while True:
        try:
            time.sleep(20)
        finally:
            print("Stopping actor")
            actor.stop()


if __name__ == "__main__":
    test()
