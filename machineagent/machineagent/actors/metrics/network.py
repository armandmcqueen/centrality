import conclib
from common import constants
from machineagent.config import MachineAgentConfig
from machineagent.actors.metrics.samplers.network import NetworkSampler
from machineagent.actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi, NetworkThroughputMeasurement
from centrality_controlplane_sdk import Throughput as ThroughputHolder
from datetime import datetime, timezone


class SendNetworkMetrics(conclib.ActorMessage):
    pass


class NetworkMetricCollector(conclib.PeriodicActor):
    URN = constants.MACHINE_AGENT_NETWORK_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendNetworkMetrics: constants.MACHINE_AGENT_METRIC_NETWORK_INTERVAL_SECS,
    }

    def __init__(
        self,
        machine_agent_config: MachineAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.machine_agent_config = machine_agent_config
        self.config = self.machine_agent_config.metrics.network
        self.control_plane_sdk = control_plane_sdk
        self.sampler = NetworkSampler()

        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_network_metric(self) -> None:
        if self.config.use_fake:
            sent_mbs = self.fake_metric_generator.sample()
            recv_mbs = self.fake_metric_generator.sample()
            iface_infos = []
            for i, (sent_mib, recv_mib) in enumerate(zip(sent_mbs, recv_mbs)):
                iface_infos.append(
                    ThroughputHolder(
                        interface_name=f"fake{i}",
                        sent_mbps=sent_mib,
                        recv_mbps=recv_mib,
                    )
                )
            total_info = ThroughputHolder(
                interface_name="total", sent_mbps=sum(sent_mbs), recv_mbps=sum(recv_mbs)
            )
            iface_infos.append(total_info)
        else:
            iface_infos, total_info = self.sampler.sample()

        # print(f"📡 {self.__class__.__name__} - sending metrics: {iface_infos}")

        measurement = NetworkThroughputMeasurement(
            machine_id=self.machine_agent_config.machine_id,
            ts=datetime.now(timezone.utc),
            per_interface=iface_infos,
            total=total_info,
        )
        self.control_plane_sdk.put_network_throughput_metric(
            network_throughput_measurement=measurement
        )

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendNetworkMetrics):
            try:
                self.send_network_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)


def test():
    FAKE = False
    import time
    from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig

    config = MachineAgentConfig()
    config.metrics.network.use_fake = FAKE
    control_plane_sdk_config = ControlPlaneSdkConfig()
    control_plane_sdk = get_sdk(
        control_plane_sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    actor = NetworkMetricCollector.start(
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
