import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.net import NetworkSampler
from actors.metrics.faketrics import FakeMetricGenerator
from centrality_controlplane_sdk import DataApi


class SendNetworkMetrics(conclib.ActorMessage):
    pass


class NetworkMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_NETWORK_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendNetworkMetrics: constants.VM_AGENT_METRIC_NETWORK_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config = self.vm_agent_config.metrics.network
        self.control_plane_sdk = control_plane_sdk
        self.sampler = NetworkSampler()

        self.fake_metric_generator = FakeMetricGenerator(self.config.fake)
        super().__init__()

    def send_network_metric(self) -> None:
        if self.config.use_fake:
            sent_mibs = self.fake_metric_generator.sample()
            recv_mibs = self.fake_metric_generator.sample()
            iface_infos = {}
            for i, (sent_mib, recv_mib) in enumerate(zip(sent_mibs, recv_mibs)):
                iface_infos[f"fake{i}"] = (sent_mib, recv_mib)
            iface_infos["total"] = (sum(sent_mibs), sum(recv_mibs))
        else:
            iface_infos = self.sampler.sample()
            # convert to dict of tuples
            iface_infos = {
                k: v.as_tuple() for k, v in iface_infos.items()
            }  # TODO: Do this in the sampler?

        print(f"📡 {self.__class__.__name__} - sending metrics: {iface_infos}")

        pass
        # measurement = CpuMeasurement(
        #     vm_id=self.vm_agent_config.vm_id,
        #     ts=datetime.datetime.now(datetime.timezone.utc),
        #     cpu_percents=cpu_percents,
        # )
        # self.control_plane_sdk.put_cpu_metric(cpu_measurement=measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendNetworkMetrics):
            try:
                self.send_network_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
