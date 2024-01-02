from controlplane.actors.datastore_sweeper import (
    DatastoreSweeperConfig,
    DatastoreSweeper,
)
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from ..utils.utils import print_test_function_name
import datetime
import time
from rich import print


VM_ID = "test-vm-id"


def test_sweeper(datastore: tuple[DatastoreConfig, DatastoreClient]):
    """
    Test that the sweeper actor deletes old data points
    """
    print_test_function_name()
    datastore_config, client = datastore

    # Add 10 old data points and 10 recent ones
    now = datetime.datetime.now(datetime.timezone.utc)
    num_metrics = 10
    timestamps = [
        now - datetime.timedelta(seconds=(i + 1) * 120) for i in range(num_metrics)
    ]
    timestamps.extend(
        [now - datetime.timedelta(seconds=i * 0.1) for i in range(num_metrics)]
    )
    for ind, ts in enumerate(timestamps):
        client.add_cpu_measurement(
            vm_id=VM_ID,
            cpu_percents=[ind, ind, ind, ind],
            ts=ts,
        )

    # Confirm that we have 20 data points
    current_data = client.get_cpu_measurements(vm_ids=[VM_ID])
    assert (
        len(current_data) == num_metrics * 2
    ), f"Expected {num_metrics * 2} data points"

    # Start the sweeper so it runs frequently and deletes the 10 old data points
    datastore_sweeper_config = DatastoreSweeperConfig(
        sweep_interval_secs=1,
        data_retention_secs=60,
    )
    sweeper = DatastoreSweeper.start(
        datastore_sweeper_config=datastore_sweeper_config,
        datastore_config=datastore_config,
    )
    try:
        time.sleep(2)

        # Confirm that we now only have 10 data points
        current_data = client.get_cpu_measurements(vm_ids=[VM_ID])
        assert (
            len(current_data) == num_metrics
        ), f"Expected {num_metrics} data points, but got {len(current_data)}"

        # Cleanup
        print("Sweeper test passed")
    finally:
        sweeper.stop()
