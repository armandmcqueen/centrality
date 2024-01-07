import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.diskio import DiskIoSampler
from vmagent.actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi


class SendDiskIoMetrics(conclib.ActorMessage):
    pass


class DiskIoMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_DISK_IO_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendDiskIoMetrics: constants.VM_AGENT_METRIC_DISK_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config = self.vm_agent_config.metrics.diskio
        self.control_plane_sdk = control_plane_sdk
        self.sampler = DiskIoSampler()
        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_disk_io_metric(self) -> None:
        if self.config.use_fake:
            iops = self.fake_metric_generator.sample()
            read_mibs = self.fake_metric_generator.sample()
            write_mibs = self.fake_metric_generator.sample()
            throughput_infos = {}
            iops_infos = {}
            for i in range(self.config.fake.num_vals):
                disk_name = f"/dev/fake{i}"
                disk_iops = iops[i]
                disk_read_mib = read_mibs[i]
                disk_write_mib = write_mibs[i]
                throughput_infos[disk_name] = (disk_read_mib, disk_write_mib)
                iops_infos[disk_name] = disk_iops
        else:
            throughput_infos, iops_infos = self.sampler.sample()

        print(
            f"📡 {self.__class__.__name__} - sending metrics: {throughput_infos, iops_infos}"
        )

        pass
        # measurement = CpuMeasurement(
        #     vm_id=self.vm_agent_config.vm_id,
        #     ts=datetime.datetime.now(datetime.timezone.utc),
        #     cpu_percents=cpu_percents,
        # )
        # self.control_plane_sdk.put_cpu_metric(cpu_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendDiskIoMetrics):
            try:
                self.send_disk_io_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)


def main():
    import time
    from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig

    config = VmAgentConfig()
    config.metrics.diskio.use_fake = False
    control_plane_sdk_config = ControlPlaneSdkConfig()
    control_plane_sdk = get_sdk(
        control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    actor = DiskIoMetricCollector.start(
        vm_agent_config=config, control_plane_sdk=control_plane_sdk
    )
    while True:
        try:
            time.sleep(20)
        finally:
            print("Stopping actor")
            actor.stop()


if __name__ == "__main__":
    main()
