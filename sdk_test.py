import pytest
import subprocess
from pathlib import Path
from centrality_controlplane_sdk import DataApi
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig
from common.utils.wait_for_healthy import wait_for_healthy
from common import constants
from common.sdks.controlplane.sdk import get_sdk
from rich import print
import time



def main():
    sdk_config = ControlPlaneSdkConfig()
    client = get_sdk(sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN)
    resp = client.get_healthcheck()
    machines = client.get_live_machines()
    print(machines)


if __name__ == '__main__':
    main()