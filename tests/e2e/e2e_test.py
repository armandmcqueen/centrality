# End-to-end tests. This has overlap with other e2e test, but the difference is
# that this file is testing e2e behavior/outcomes, while the others are testing
# component behavior while using the E2E infrastructure.

from datetime import datetime, timezone
from centrality_controlplane_sdk import DataApi, ApiException
from rich import print
from ..utils.utils import print_test_function_name
from ..utils.parameterized_metrics_sdk import (
    MetricType,
    get_latest_metric_sdk,
    validate_measurement_is_sane,
)
from ..utils import asserts
from common import constants
from . import constants as test_constants
import pytest


def test_healthcheck(docker_compose, sdk: DataApi):
    """Confirm we can hit the healthcheck endpoint and it returns a 200"""
    r = sdk.get_healthcheck()
    assert r.status == "ok", f"Healthcheck is not 'ok': {r}"

    r = sdk.get_auth_healthcheck()
    assert r.status == "ok", f"Auth healthcheck is not 'ok': {r}"


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


def test_live_machines(docker_compose, sdk: DataApi):
    """
    Check if the live machines endpoint is working correctly. Implicitly checks if the
    agents are sending heartbeats correctly.
    """
    print_test_function_name()

    live_machines = sdk.get_live_machines()
    asserts.list_size(live_machines, test_constants.EXPECTED_NUM_AGENTS)

    # Find the machine info with id = constants.FAKE_AGENT_ID
    fake_machine = [
        m for m in live_machines if m.machine_id == test_constants.FAKE_AGENT_ID
    ]
    asserts.list_size(fake_machine, 1)
    fake_machine = fake_machine[0]

    # Check that the machine info is correct
    asserts.matches(fake_machine.machine_id, test_constants.FAKE_AGENT_ID)
    asserts.matches(fake_machine.num_cpus, 8)
    asserts.matches(
        fake_machine.cpu_description, "Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz"
    )
    asserts.matches(fake_machine.host_memory_mb, 16000)
    asserts.matches(fake_machine.num_gpus, 8)
    asserts.matches(fake_machine.gpu_type, "NVIDIA A100")
    asserts.matches(fake_machine.gpu_memory_mb, 60000)
    asserts.matches(fake_machine.nvidia_driver_version, "535.129.03")


@pytest.mark.parametrize("metric_type", MetricType)
def test_get_latest_metrics(docker_compose, sdk, metric_type: MetricType):
    """
    Check if the get latest cpu measurements endpoint is working correctly.
    """
    print_test_function_name(additional_info=metric_type)
    live_machines = [m.machine_id for m in sdk.get_live_machines()]
    print(live_machines)
    measurements = get_latest_metric_sdk(metric_type, sdk, live_machines)
    if metric_type not in [MetricType.GPU_MEMORY, MetricType.GPU_UTILIZATION]:
        # Not all nodes have GPUs
        # TODO: Parse which nodes have GPUs and check that we have that many latest metrics
        asserts.same_size(measurements, live_machines)

    for m in measurements:
        validate_measurement_is_sane(metric_type, m)

        # check that ts was within the last MACHINE_HEARTBEAT_TIMEOUT_SECS seconds
        assert (
            datetime.now(timezone.utc) - m.ts
        ).total_seconds() < constants.MACHINE_NO_HEARTBEAT_LIMBO_SECS, (
            f"measurement timestamp was not within the last "
            f"{constants.MACHINE_NO_HEARTBEAT_LIMBO_SECS} seconds: "
            f"{m.ts}"
        )


# TODO: test e2e datastore sweeper (metric deletion and machine reaping)
