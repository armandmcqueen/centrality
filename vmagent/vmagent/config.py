import pydantic
from common.config.config import CentralityConfig
from vmagent.rest.config import VmAgentRestConfig
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig


class VmAgentConfig(CentralityConfig):
    vm_id: str
    rest: VmAgentRestConfig = pydantic.Field(default_factory=VmAgentRestConfig)
    controlplane_sdk: ControlPlaneSdkConfig = pydantic.Field(default_factory=ControlPlaneSdkConfig)



