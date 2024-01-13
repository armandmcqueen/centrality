from common.sdks.controlplane.sdk import ControlPlaneSdkConfig, get_sdk
from pydantic import BaseModel
from common import constants
import requests
from rich.console import Console
from centrality_controlplane_sdk import DataApi
import time

console = Console()


class PagerDutyAlerter:
    def __init__(self):
        # TODO: Validate that the environment variables are set correctly
        pass

    def alert(self, msg: str):
        # TODO: Implement proper
        console.log(msg)


class FailedHealthcheckError(Exception):
    pass


class StreamlitConfig(BaseModel):
    host: str = "localhost"
    port: int = 8501
    https: bool = False

    @property
    def host_str(self) -> str:
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.host}:{self.port}"


def run_control_plane_healthcheck(sdk: DataApi):
    try:
        sdk.get_healthcheck()
        assert len(sdk.get_live_machines()) > 0
        console.log("✅  Control plane is healthy")
    except Exception as e:
        raise FailedHealthcheckError(f"Control plane healthcheck failed: {e}")


def run_streamlit_healthcheck(config: StreamlitConfig):
    try:
        response = requests.get(f"{config.host_str}/healthz")
        assert response.status_code == 200
        console.log("✅  Streamlit is healthy")
    except Exception as e:
        raise FailedHealthcheckError(f"Streamlit healthcheck failed: {e}")


def main(
    control_plane_config: ControlPlaneSdkConfig,
    streamlit_config: StreamlitConfig,
    healthcheck_interval: int,
):
    sdk = get_sdk(control_plane_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN)
    alerter = PagerDutyAlerter()

    while True:
        try:
            run_control_plane_healthcheck(sdk)
        except FailedHealthcheckError as e:
            alerter.alert(f"❌️ {e}")
        except Exception as e:
            alerter.alert(
                f"❌️ Unexpected error while healthchecking control plane: {e}"
            )

        try:
            run_streamlit_healthcheck(streamlit_config)
        except FailedHealthcheckError as e:
            alerter.alert(f"❌️ {e}")
        except Exception as e:
            alerter.alert(f"❌️ Unexpected error while healthchecking streamlit: {e}")
        finally:
            time.sleep(healthcheck_interval)


if __name__ == "__main__":
    config = ControlPlaneSdkConfig(
        host="localhost",
        port=8000,
        https=False,
    )
    streamlit_config = StreamlitConfig(
        host="localhost",
        port=8501,
        https=False,
    )

    main(config, streamlit_config, healthcheck_interval=5)
