import datetime
from centrality_controlplane_sdk import DataApi
from rich import print
from ..utils.utils import print_test_function_name


# TODO: This is duplicative with sdk_v2_test
def test_live_vms(docker_compose, sdk_v2: DataApi):
    """
    Check if the live vms endpoint is working correctly. Implicitly checks if the
    agents are sending heartbeats correctly.
    """
    print_test_function_name()

    live_vms = sdk_v2.list_live_vms()
    assert len(live_vms) == 4, f"Expected 4 live vms, got {len(live_vms)}"


# TODO: This is duplicative with sdk_v2_test
def test_get_latest_cpu_metrics(docker_compose, sdk_v2):
    """
    Check if the get latest cpu measurements endpoint is working correctly.
    """
    print_test_function_name()

    live_vms = sdk_v2.list_live_vms()
    print(live_vms)
    cpu_measurements = sdk_v2.get_latest_cpu_metrics(vm_ids=live_vms)
    assert (
        len(cpu_measurements) == 4
    ), f"Expected 4 cpu measurements, got {len(cpu_measurements)}"
    for cpu_measurement in cpu_measurements:
        assert len(cpu_measurement.cpu_percents) > 0, "CPU usage was empty"
        # check that ts was within the last 30 seconds
        now = datetime.datetime.now(datetime.timezone.utc)
        assert (
            (now - cpu_measurement.ts).total_seconds() < 30
        ), f"CPU measurement timestamp was not within the last 30 seconds: {cpu_measurement.ts}"


# TODO: test e2e datastore sweeper
