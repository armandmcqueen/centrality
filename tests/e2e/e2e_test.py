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


def test_live_vms(docker_compose, sdk: DataApi):
    """
    Check if the live vms endpoint is working correctly. Implicitly checks if the
    agents are sending heartbeats correctly.
    """
    print_test_function_name()

    live_vms = sdk.list_live_vms()
    asserts.list_size(live_vms, test_constants.EXPECTED_NUM_AGENTS)


@pytest.mark.parametrize("metric_type", MetricType)
def test_get_latest_metrics(docker_compose, sdk, metric_type: MetricType):
    """
    Check if the get latest cpu measurements endpoint is working correctly.
    """
    print_test_function_name()

    live_vms = sdk.list_live_vms()
    print(live_vms)
    measurements = get_latest_metric_sdk(metric_type, sdk, live_vms)
    if metric_type not in [MetricType.GPU_MEMORY, MetricType.GPU_UTILIZATION]:
        # Not all nodes have GPUs
        # TODO: Parse which nodes have GPUs and check that we have that many latest metrics
        asserts.same_size(measurements, live_vms)

    for m in measurements:
        validate_measurement_is_sane(metric_type, m)

        # check that ts was within the last VM_HEARTBEAT_TIMEOUT_SECS seconds
        assert (
            datetime.now(timezone.utc) - m.ts
        ).total_seconds() < constants.VM_NO_HEARTBEAT_LIMBO_SECS, (
            f"measurement timestamp was not within the last "
            f"{constants.VM_NO_HEARTBEAT_LIMBO_SECS} seconds: "
            f"{m.ts}"
        )


# TODO: test e2e datastore sweeper (metric deletion and vm reaping)
