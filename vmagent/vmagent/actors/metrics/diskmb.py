import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.diskmb import DiskMbSampler
from actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi


class SendDiskMbMetrics(conclib.ActorMessage):
    pass


class DiskMbMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_DISK_MB_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendDiskMbMetrics: constants.VM_AGENT_METRIC_DISK_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config = self.vm_agent_config.metrics.diskmb
        self.control_plane_sdk = control_plane_sdk
        self.sampler = DiskMbSampler()
        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_disk_mb_metric(self) -> None:
        if self.config.use_fake:
            used_mibs = self.fake_metric_generator.sample()
            disk_infos = {}
            for i, used_mib in enumerate(used_mibs):
                disk_infos[f"/dev/fake{i}"] = (used_mib, self.config.fake.max_val)
        else:
            disk_infos = self.sampler.sample()

        print(f"📡 {self.__class__.__name__} - sending metrics: {disk_infos}")

        pass
        # measurement = CpuMeasurement(
        #     vm_id=self.vm_agent_config.vm_id,
        #     ts=datetime.datetime.now(datetime.timezone.utc),
        #     cpu_percents=cpu_percents,
        # )
        # self.control_plane_sdk.put_cpu_metric(cpu_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendDiskMbMetrics):
            try:
                self.send_disk_mb_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
