from common.config.config import CentralityConfig
import centrality_controlplane_sdk as controlplane_sdk


class ControlPlaneSdkConfig(CentralityConfig):
    host: str = "localhost"
    port: int = 8000
    https: bool = False

    @property
    def host_str(self) -> str:
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.host}:{self.port}"


def get_sdk(config: ControlPlaneSdkConfig, token: str) -> controlplane_sdk.DataApi:
    """
    Get the OpenAPI generated SDK (the DataApi object), correctly configured.
    """
    configuration = controlplane_sdk.Configuration(
        host=config.host_str,
        access_token=token,
    )
    api_client = controlplane_sdk.ApiClient(configuration)
    api_instance = controlplane_sdk.DataApi(api_client)
    return api_instance
