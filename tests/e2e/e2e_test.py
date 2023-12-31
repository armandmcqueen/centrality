import datetime
from rich import print
import inspect


def print_test_function_name():
    fname = inspect.stack()[1][3]
    print(f"\nLogs for: [magenta]{fname}")


def test_live_vms(docker_compose, sdk):
    """
    Check if the live vms endpoint is working correctly. Implicitly checks if the
    agents are sending heartbeats correctly.
    """
    print_test_function_name()

    resp, live_vms = sdk.get_live_vms()
    assert resp.status_code == 200, "Failed to get live vms from control plane"
    assert len(live_vms) == 4, f"Expected 4 live vms, got {len(live_vms)}"


def test_get_latest_cpu_measurements(docker_compose, sdk):
    """
    Check if the get latest cpu measurements endpoint is working correctly.
    """
    print_test_function_name()

    resp, live_vms = sdk.get_live_vms()
    print(live_vms)
    resp, cpu_measurements = sdk.get_latest_cpu_measurements(vm_ids=live_vms)
    assert resp.status_code == 200, "Failed to get cpu measurements from control plane"
    assert (
        len(cpu_measurements) == 4
    ), f"Expected 4 cpu measurements, got {len(cpu_measurements)}"
    for cpu_measurement in cpu_measurements:
        assert len(cpu_measurement.cpu_usage) > 0, "CPU usage was empty"
        # check that ts was within the last 30 seconds
        now = datetime.datetime.now(datetime.timezone.utc)
        assert (
            (now - cpu_measurement.ts).total_seconds() < 30
        ), f"CPU measurement timestamp was not within the last 30 seconds: {cpu_measurement.ts}"
