import uuid

from typing import Optional
import pykka

from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.cpu import CpuMetricCollector
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig


class ActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """
    def __init__(
            self,
            vm_id: str,
            control_plane_sdk_config: ControlPlaneSdkConfig,
            control_plane_sdk_token: str,
    ):
        self.control_plane_sdk_config = control_plane_sdk_config
        self.vm_agent_config = VmAgentConfig(vm_id=vm_id)

        self.metric_subsystem = MetricSubsystem(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk_config=control_plane_sdk_config,
            control_plane_sdk_token=control_plane_sdk_token,

        )

    def start(self):
        self.metric_subsystem.start()


class MetricSubsystem:
    """
    Container for all the metric actors
    """
    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk_config: ControlPlaneSdkConfig,
            control_plane_sdk_token: str,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk_config = control_plane_sdk_config
        self.control_plane_sdk_token = control_plane_sdk_token
        self.cpu_metric_collector_ref: Optional[pykka.ActorRef] = None

    def start(self):
        self.cpu_metric_collector_ref = CpuMetricCollector.start(
            vm_agent_config=self.vm_agent_config,
            control_plane_sdk_config=self.control_plane_sdk_config,
            control_plane_sdk_token=self.control_plane_sdk_token,
        )
