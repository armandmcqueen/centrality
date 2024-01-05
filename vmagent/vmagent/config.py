import uuid

from pydantic import Field
from common.config.config import CentralityConfig
from vmagent.rest.config import VmAgentRestConfig
from vmagent.actors.metrics.config import MetricsConfig
from vmagent.machineinfo.config import MachineInfoConfig
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig


class VmAgentConfig(CentralityConfig):
    vm_id: str = Field(default_factory=lambda: f"vm-{uuid.uuid4()}")
    rest: VmAgentRestConfig = Field(default_factory=VmAgentRestConfig)
    controlplane_sdk: ControlPlaneSdkConfig = Field(
        default_factory=ControlPlaneSdkConfig
    )
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    machine_info: MachineInfoConfig = Field(default_factory=MachineInfoConfig)
