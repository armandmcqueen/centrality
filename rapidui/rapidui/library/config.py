from common.config.config import CentralityConfig
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig
from pydantic import Field


class StreamlitUiConfig(CentralityConfig):
    control_plane_sdk: ControlPlaneSdkConfig = Field(
        default_factory=ControlPlaneSdkConfig
    )
    live_vm_interval_ms: int = 5000
    metric_interval_ms: int = 200
