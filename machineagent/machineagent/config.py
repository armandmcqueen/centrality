import uuid

from pydantic import Field
from common.config.config import CentralityConfig
from machineagent.rest.config import VmAgentRestConfig
from machineagent.actors.metrics.config import MetricsConfig
from machineagent.machineinfo.config import MachineInfoConfig
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig


class MachineAgentConfig(CentralityConfig):
    machine_id: str = Field(default_factory=lambda: f"machine-{uuid.uuid4()}")
    rest: VmAgentRestConfig = Field(default_factory=VmAgentRestConfig)
    controlplane_sdk: ControlPlaneSdkConfig = Field(
        default_factory=ControlPlaneSdkConfig
    )
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    machine_info: MachineInfoConfig = Field(default_factory=MachineInfoConfig)
