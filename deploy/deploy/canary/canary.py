from common.sdks.controlplane.sdk import ControlPlaneSdkConfig, get_sdk
from pydantic import BaseModel
from common import constants
import requests
from rich.console import Console
from centrality_controlplane_sdk import DataApi
import time

from pdpyras import EventsAPISession
import os
import typer


PAGER_DUTY_URL = "https://events.pagerduty.com/v2/enqueue"
INTEGRATION_KEY_ENV_VAR = "PAGERDUTY_INTEGRATION_KEY"

app = typer.Typer()

console = Console()


class Alerter:
    def alert(self, msg: str):
        raise NotImplementedError()


class PrintAlert(Alerter):
    def __init__(self, source: str):
        self.source = source

    def alert(self, msg: str):
        console.log(f"❗️ Alert from {self.source}: {msg}")


class PagerDutyAlerter(Alerter):
    def __init__(self, source: str):
        if INTEGRATION_KEY_ENV_VAR not in os.environ:
            raise ValueError(f"Environment variable {INTEGRATION_KEY_ENV_VAR} not set")
        self.source = source
        self.integration_key = os.environ[INTEGRATION_KEY_ENV_VAR]
        self.session = EventsAPISession(self.integration_key)

    def alert(self, msg: str):
        try:
            self.session.trigger(summary=msg, source=self.source, severity="error")
            console.log(
                f"❗️ Healthcheck failed. Alert sent to PagerDuty. Healthcheck details: {msg}"
            )
        except Exception as e:
            console.log(f"❗️❗️❗️ Failed to send alert to PagerDuty: {e}")


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
        if len(sdk.get_live_machines()) <= 0:
            raise FailedHealthcheckError("no live machines")
        console.log(
            f"✅  Control plane is healthy ( {sdk.api_client.configuration.host} )"
        )
    except Exception as e:
        raise FailedHealthcheckError(
            f"Control plane healthcheck failed ( {sdk.api_client.configuration.host} ): {e}"
        )


def run_streamlit_healthcheck(config: StreamlitConfig):
    try:
        response = requests.get(f"{config.host_str}/healthz")
        if response.status_code != 200:
            raise FailedHealthcheckError(f"Response code not 200: {response}")
        console.log(f"✅  Streamlit is healthy ( {config.host_str} )")
    except Exception as e:
        raise FailedHealthcheckError(
            f"Streamlit healthcheck failed ( {config.host_str} ): {e}"
        )


@app.command(
    help="Run a canary that checks the health of the control plane and streamlit."
)
def main(
    mode: str = typer.Argument(
        help="The mode to run the canary in. Either 'localhost' or 'prod'."
    ),
    pagerduty: bool = typer.Option(
        False,
        help="Whether to send alerts to PagerDuty or not. If no, will print alerts to stdout.",
    ),
):
    assert mode in [
        "localhost",
        "prod",
    ], f"Unknown mode '{mode}'. Only 'localhost' and 'prod' are supported."

    if mode == "localhost":
        control_plane_config = ControlPlaneSdkConfig(
            host="localhost",
            port=8000,
            https=False,
        )
        streamlit_config = StreamlitConfig(
            host="localhost",
            port=8501,
            https=False,
        )
    elif mode == "prod":
        control_plane_config = ControlPlaneSdkConfig(
            host="centrality-dev.fly.dev",
            port=8000,
            https=True,
        )
        streamlit_config = StreamlitConfig(
            host="centrality-dev.fly.dev",
            port=443,
            https=True,
        )
    else:
        raise NotImplementedError(f"Unknown mode {mode}")

    if pagerduty:
        alerter = PagerDutyAlerter(source=f"canary-{mode}")
    else:
        alerter = PrintAlert(source=f"canary-{mode}")

    main_loop(
        control_plane_config=control_plane_config,
        streamlit_config=streamlit_config,
        healthcheck_interval=5,
        alerter=alerter,
    )


def main_loop(
    control_plane_config: ControlPlaneSdkConfig,
    streamlit_config: StreamlitConfig,
    healthcheck_interval: int,
    alerter: Alerter,
):
    sdk = get_sdk(control_plane_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN)

    while True:
        try:
            run_control_plane_healthcheck(sdk)
        except FailedHealthcheckError as e:
            alerter.alert(f"{e}")
        except Exception as e:
            alerter.alert(f"Unexpected error while healthchecking control plane: {e}")

        try:
            run_streamlit_healthcheck(streamlit_config)
        except FailedHealthcheckError as e:
            alerter.alert(f"{e}")
        except Exception as e:
            alerter.alert(f"Unexpected error while healthchecking streamlit: {e}")
        finally:
            time.sleep(healthcheck_interval)


if __name__ == "__main__":
    app()
