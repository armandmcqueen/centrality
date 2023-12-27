import pykka

from typing import Optional

from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.cpu import CpuMetricCollector
from vmagent.actors.heartbeat import HeartbeatSender
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk


class VmAgentActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """
    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk

        self.metric_subsystem = MetricSubsystem(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
        self.heartbeat_sender_ref: Optional[pykka.ActorRef] = None

    def start(self) -> "VmAgentActorSystem":
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
            control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk
        self.cpu_metric_collector_ref: Optional[pykka.ActorRef] = None

    def start(self):
        self.cpu_metric_collector_ref = CpuMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk=self.control_plane_sdk,
        )
