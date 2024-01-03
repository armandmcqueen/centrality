from common.config.config import CentralityConfig
import centrality_controlplane_sdk as controlplane_sdk
from typing import Optional


class ControlPlaneSdkConfig(CentralityConfig):
    host: str = "localhost"
    port: int = 8000
    https: bool = False

    @property
    def host_str(self) -> str:
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.host}:{self.port}"


def get_sdk(
    config: ControlPlaneSdkConfig, token: str, disable_auth: Optional[bool] = False
) -> controlplane_sdk.DataApi:
    """
    Get the OpenAPI generated SDK (the DataApi object), correctly configured.
    """
    configuration = controlplane_sdk.Configuration(
        host=config.host_str,
    )
    if not disable_auth:
        configuration.access_token = token

    api_client = controlplane_sdk.ApiClient(configuration)
    api_instance = controlplane_sdk.DataApi(api_client)
    return api_instance
