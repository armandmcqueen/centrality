import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.memory import MemorySampler
from vmagent.actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi, MemoryMeasurement
from datetime import datetime, timezone


class SendMemoryMetrics(conclib.ActorMessage):
    pass


class MemoryMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_MEMORY_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendMemoryMetrics: constants.VM_AGENT_METRIC_MEMORY_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config = self.vm_agent_config.metrics.memory
        self.control_plane_sdk = control_plane_sdk
        self.sampler = MemorySampler()

        if self.config.fake.num_vals != 1:
            raise ValueError(
                "MemoryMetricConfig.fake.num_vals must be 1 for MemoryMetricCollector - there's only one memory metric!"
            )

        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_memory_metric(self) -> None:
        if self.config.use_fake:
            total_mem_mib = self.config.fake.max_val
            free_mem_mib = self.fake_metric_generator.sample()[0]
        else:
            free_mem_mib, total_mem_mib = self.sampler.sample()

        # print(
        #     f"{self.__class__.__name__} - sending memory metric: {int(free_mem_mib)} MiB free / {int(total_mem_mib)} MiB total"
        # )
        measurement = MemoryMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.now(timezone.utc),
            free_memory_mb=free_mem_mib,
            total_memory_mb=total_mem_mib,
        )
        self.control_plane_sdk.put_memory_metric(memory_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendMemoryMetrics):
            try:
                self.send_memory_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)


def test():
    FAKE = True
    import time
    from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig

    config = VmAgentConfig()
    config.metrics.memory.use_fake = FAKE
    control_plane_sdk_config = ControlPlaneSdkConfig()
    control_plane_sdk = get_sdk(
        control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    actor = MemoryMetricCollector.start(
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
