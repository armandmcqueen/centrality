# End-to-end tests. This has overlap with other e2e test, but the difference is
# that this file is testing e2e behavior/outcomes, while the others are testing
# component behavior while using the E2E infrastructure.

import datetime
from centrality_controlplane_sdk import DataApi, ApiException
from rich import print
from ..utils.utils import print_test_function_name
from common import constants
import pytest


def test_healthcheck(docker_compose, sdk: DataApi):
    """Confirm we can hit the healthcheck endpoint and it returns a 200"""
    health_resp = sdk.get_healthcheck()
    assert health_resp.status == "ok", f"Healthcheck is not 'ok': {health_resp}"

    health_auth_resp = sdk.get_auth_healthcheck()
    assert (
        health_auth_resp.status == "ok"
    ), f"Auth healthcheck is not 'ok': {health_resp}"


def test_auth(docker_compose, unauthed_sdk: DataApi):
    """
    Test that we can hit the healthcheck with an unauthed client, but get rejected
    if we try to hit an authorized endpoint
    """
    health_resp = unauthed_sdk.get_healthcheck()
    assert health_resp.status == "ok", f"Healthcheck is not 'ok': {health_resp}"

    with pytest.raises(ApiException) as e:  # type: ApiException
        _ = unauthed_sdk.get_auth_healthcheck()
        assert e.status == 403, f"Expected 403 error code, got {e.status}"


def test_live_vms(docker_compose, sdk: DataApi):
    """
    Check if the live vms endpoint is working correctly. Implicitly checks if the
    agents are sending heartbeats correctly.
    """
    print_test_function_name()

    live_vms = sdk.list_live_vms()
    assert len(live_vms) == 4, f"Expected 4 live vms, got {len(live_vms)}"


def test_get_latest_cpu_metrics(docker_compose, sdk):
    """
    Check if the get latest cpu measurements endpoint is working correctly.
    """
    print_test_function_name()

    live_vms = sdk.list_live_vms()
    print(live_vms)
    cpu_measurements = sdk.get_latest_cpu_metrics(vm_ids=live_vms)
    assert len(cpu_measurements) == len(
        live_vms
    ), f"Expected {len(live_vms)} cpu measurements, got {len(cpu_measurements)}"
    for cpu_measurement in cpu_measurements:
        assert len(cpu_measurement.cpu_percents) > 0, "CPU usage was empty"
        # check that ts was within the last VM_HEARTBEAT_TIMEOUT_SECS seconds
        now = datetime.datetime.now(datetime.timezone.utc)
        assert (
            now - cpu_measurement.ts
        ).total_seconds() < constants.VM_HEARTBEAT_TIMEOUT_SECS, (
            f"CPU measurement timestamp was not within the last "
            f"{constants.VM_HEARTBEAT_TIMEOUT_SECS} seconds: "
            f"{cpu_measurement.ts}"
        )


# TODO: test e2e datastore sweeper
