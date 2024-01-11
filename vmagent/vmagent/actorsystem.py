import pykka

from typing import Optional

from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.cpu import CpuMetricCollector
from vmagent.actors.metrics.diskio import DiskIoMetricCollector
from vmagent.actors.metrics.diskmb import DiskUsageMetricCollector
from vmagent.actors.metrics.gpu import GpuMetricCollector
from vmagent.actors.metrics.memory import MemoryMetricCollector
from vmagent.actors.metrics.network import NetworkMetricCollector
from vmagent.actors.metrics.nvidia_smi import NvidiaSmiMetricCollector
from vmagent.actors.heartbeat import HeartbeatSender
from vmagent.machineinfo.machineinfo import get_machine_info
from centrality_controlplane_sdk import DataApi


class VmAgentActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk

        self.metric_subsystem = MetricSubsystem(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.heartbeat_sender_ref: Optional[pykka.ActorRef] = None

    def start(self) -> "VmAgentActorSystem":
        registration_info = get_machine_info(self.vm_agent_config.machine_info)
        print(f"📋 Registering VM with info: {registration_info}")
        self.control_plane_sdk.register_vm(
            vm_registration_info=registration_info, vm_id=self.vm_agent_config.vm_id
        )

        self.metric_subsystem.start()
        self.heartbeat_sender_ref = HeartbeatSender.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        return self


class MetricSubsystem:
    """
    Container for all the metric actors
    """

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
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
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.disk_io_metric_collector_ref = DiskIoMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.disk_mb_metric_collector_ref = DiskUsageMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.gpu_metric_collector_ref = GpuMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.memory_metric_collector_ref = MemoryMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.network_metric_collector_ref = NetworkMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.nvidia_smi_metric_collector_ref = NvidiaSmiMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
