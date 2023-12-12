import datetime
import time

from controlplane.datastore.client import DatastoreClient
from controlplane.datastore.config import DefaultDatastoreConfig


def test_token(client: DatastoreClient):
    generated_token = client.new_token()
    print(f"New token generated: {generated_token}")
    existing_tokens = client.get_tokens()
    for token in existing_tokens:
        print(f"Existing token: {token}")

    authed = client.validate_token("dev")
    print(f"Authed: {authed}")


def test_metrics(client: DatastoreClient):
    """Add some metrics and then retrieve them. Test retrieval filtering by time"""
    vm_id = "examplevm"
    start_time = None
    end_time = None
    print("Adding metrics", end="", flush=True)
    for i in range(10):
        metric_vals = [i + 0.1, i + 0.2, i + 0.3, i + 0.4, i + 0.5]
        ts = datetime.datetime.utcnow()
        print(".", end="", flush=True)
        time.sleep(0.1)
        if start_time is None:
            start_time = ts
        end_time = ts
        client.add_cpu_measurement(vm_id=vm_id, cpu_percents=metric_vals, ts=ts)
    print(flush=True)

    # Retrieve all metrics for the vm
    print()
    print("Testing get_cpu_measurements with no time filters")
    all_metrics = client.get_cpu_measurements(vm_ids=[vm_id], start_ts=None, end_ts=None)
    expected = 10
    matched = len(all_metrics) == expected
    output = "PASSED" if matched else "FAILED"
    print(f"[{output}] Expected {expected}, got: {len(all_metrics)}")

    print()
    print("Testing get_cpu_measurements with start and end time filters, inclusive")
    all_metrics_defined = client.get_cpu_measurements(
        vm_ids=[vm_id], start_ts=start_time, end_ts=end_time
    )
    # print(all_metrics_defined)
    expected = 10
    matched = len(all_metrics_defined) == expected
    output = "PASSED" if matched else "FAILED"
    print(f"[{output}] Expected {expected}, got: {len(all_metrics_defined)}")

    # Get half of the measurements
    print()
    print("Testing get_cpu_measurements with end_filter")
    first_half_metrics = client.get_cpu_measurements(
        vm_ids=[vm_id],
        start_ts=start_time,
        end_ts=start_time + datetime.timedelta(seconds=0.5),
    )
    # print(first_half_metrics)
    expected = 5
    matched = len(first_half_metrics) == expected
    output = "PASSED" if matched else "FAILED"
    print(
        f"[{output}] Expected {expected}, got: {len(first_half_metrics)} (test is potentially flaky)"
    )

    # Get the other half of the measurements
    print()
    print("Testing get_cpu_measurements with start filter")
    second_half_metrics = client.get_cpu_measurements(
        vm_ids=[vm_id],
        start_ts=start_time + datetime.timedelta(seconds=0.5),
        end_ts=end_time,
    )
    # print(second_half_metrics)
    expected = 5
    matched = len(second_half_metrics) == expected
    output = "PASSED" if matched else "FAILED"
    print(
        f"[{output}] Expected 5, got: {len(second_half_metrics)} (test is potentially flaky)"
    )


if __name__ == "__main__":
    config = DefaultDatastoreConfig()
    client = DatastoreClient(config)
    client.reset_db()

    # test_token(client=client)
    test_metrics(client=client)
