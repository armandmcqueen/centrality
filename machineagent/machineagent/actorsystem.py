import pykka

from typing import Optional

from machineagent.config import MachineAgentConfig
from machineagent.actors.metrics.cpu import CpuMetricCollector
from machineagent.actors.metrics.diskio import DiskIoMetricCollector
from machineagent.actors.metrics.diskmb import DiskUsageMetricCollector
from machineagent.actors.metrics.gpu import GpuMetricCollector
from machineagent.actors.metrics.memory import MemoryMetricCollector
from machineagent.actors.metrics.network import NetworkMetricCollector
from machineagent.actors.metrics.nvidia_smi import NvidiaSmiMetricCollector
from machineagent.actors.heartbeat import HeartbeatSender
from machineagent.machineinfo.machineinfo import get_machine_info
from centrality_controlplane_sdk import DataApi


class VmAgentActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """

    def __init__(
        self,
        machine_agent_config: MachineAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.machine_agent_config = machine_agent_config
        self.control_plane_sdk = control_plane_sdk

        self.metric_subsystem = MetricSubsystem(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.heartbeat_sender_ref: Optional[pykka.ActorRef] = None

    def start(self) -> "VmAgentActorSystem":
        registration_info = get_machine_info(self.machine_agent_config.machine_info)
        print(f"📋 Registering VM with info: {registration_info}")
        self.control_plane_sdk.register_machine(
            machine_registration_info=registration_info,
            machine_id=self.machine_agent_config.machine_id,
        )

        self.metric_subsystem.start()
        self.heartbeat_sender_ref = HeartbeatSender.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        return self


class MetricSubsystem:
    """
    Container for all the metric actors
    """

    def __init__(
        self,
        machine_agent_config: MachineAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.machine_agent_config = machine_agent_config
        self.control_plane_sdk = control_plane_sdk
        self.cpu_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.disk_io_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.disk_mb_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.gpu_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.memory_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.network_metric_collector_ref: Optional[pykka.ActorRef] = None
        self.nvidia_smi_metric_collector_ref: Optional[pykka.ActorRef] = None

    def start(self):
        self.cpu_metric_collector_ref = CpuMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.disk_io_metric_collector_ref = DiskIoMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.disk_mb_metric_collector_ref = DiskUsageMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.gpu_metric_collector_ref = GpuMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.memory_metric_collector_ref = MemoryMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.network_metric_collector_ref = NetworkMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.nvidia_smi_metric_collector_ref = NvidiaSmiMetricCollector.start(
            machine_agent_config=self.machine_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
