import conclib
from common import constants
from machineagent.config import MachineAgentConfig
from machineagent.actors.metrics.samplers.diskmb import DiskMbSampler
from machineagent.actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi, DiskUsageMeasurement, DiskUsage
from datetime import datetime, timezone


class SendDiskMbMetrics(conclib.ActorMessage):
    pass


class DiskUsageMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_DISK_MB_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendDiskMbMetrics: constants.VM_AGENT_METRIC_DISK_INTERVAL_SECS,
    }

    def __init__(
        self,
        machine_agent_config: MachineAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.machine_agent_config = machine_agent_config
        self.config = self.machine_agent_config.metrics.disk_usage
        self.control_plane_sdk = control_plane_sdk
        self.sampler = DiskMbSampler()
        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_disk_mb_metric(self) -> None:
        if self.config.use_fake:
            used_mibs = self.fake_metric_generator.sample()
            disk_infos = []
            for i, used_mib in enumerate(used_mibs):
                d = DiskUsage(
                    disk_name=f"/dev/fake{i}",
                    used_mb=used_mib,
                    total_mb=self.config.fake.max_val,
                )
                disk_infos.append(d)

        else:
            disk_infos = self.sampler.sample()

        # print(f"📡 {self.__class__.__name__} - sending metrics: {disk_infos}")

        measurement = DiskUsageMeasurement(
            machine_id=self.machine_agent_config.machine_id,
            ts=datetime.now(timezone.utc),
            usage=disk_infos,
        )
        self.control_plane_sdk.put_disk_usage_metric(disk_usage_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendDiskMbMetrics):
            try:
                self.send_disk_mb_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)


def test():
    FAKE = True
    import time
    from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig

    config = MachineAgentConfig()
    config.metrics.disk_usage.use_fake = FAKE
    control_plane_sdk_config = ControlPlaneSdkConfig()
    control_plane_sdk = get_sdk(
        control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    actor = DiskUsageMetricCollector.start(
        machine_agent_config=config, control_plane_sdk=control_plane_sdk
    )
    while True:
        try:
            time.sleep(20)
        finally:
            print("Stopping actor")
            actor.stop()


if __name__ == "__main__":
    test()
