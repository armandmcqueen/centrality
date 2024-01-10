import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.diskio import DiskIoSampler
from vmagent.actors.metrics.faketrics import FakeMetricGenerator
from datetime import datetime, timezone
from centrality_controlplane_sdk import (
    DataApi,
    DiskIopsMeasurement,
    DiskThroughputMeasurement,
)
from centrality_controlplane_sdk import DiskThroughput as DiskThroughputHolder
from centrality_controlplane_sdk import DiskIops as DiskIopsHolder


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
        self.throughput_config = self.vm_agent_config.metrics.disk_throughput
        self.iops_config = self.vm_agent_config.metrics.disk_iops
        self.control_plane_sdk = control_plane_sdk
        self.sampler = DiskIoSampler()
        self.fake_metric_generator_throughput = FakeMetricGenerator(
            self.throughput_config.fake
        )
        self.fake_metric_generator_iops = FakeMetricGenerator(self.iops_config.fake)
        super().__init__()

    def send_disk_io_metric(self) -> None:
        if self.throughput_config.use_fake:
            iops = self.fake_metric_generator_iops.sample()
            read_mbs = self.fake_metric_generator_throughput.sample()
            write_mbs = self.fake_metric_generator_throughput.sample()
            throughput_infos = []
            iops_infos = []
            for i in range(self.throughput_config.fake.num_vals):
                disk_name = f"/dev/fake{i}"
                disk_iops = iops[i]
                disk_read_mib = read_mbs[i]
                disk_write_mib = write_mbs[i]
                throughput_infos.append(
                    DiskThroughputHolder(
                        disk_name=disk_name,
                        read_mbps=disk_read_mib,
                        write_mbps=disk_write_mib,
                    )
                )
                iops_infos.append(DiskIopsHolder(disk_name=disk_name, iops=disk_iops))
        else:
            throughput_infos, iops_infos = self.sampler.sample()

        iops_measurement = DiskIopsMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.now(timezone.utc),
            iops=iops_infos,
        )
        throughput_measurement = DiskThroughputMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.now(timezone.utc),
            throughput=throughput_infos,
        )
        self.control_plane_sdk.put_disk_iops_metric(
            disk_iops_measurement=iops_measurement
        )
        self.control_plane_sdk.put_disk_throughput_metric(
            disk_throughput_measurement=throughput_measurement
        )

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

    FAKE = False
    config = VmAgentConfig()
    config.metrics.disk_throughput.use_fake = FAKE
    config.metrics.disk_iops.use_fake = FAKE
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
