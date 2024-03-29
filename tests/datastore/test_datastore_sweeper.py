from controlplane.actors.datastore_sweeper import (
    DatastoreSweeperConfig,
    DatastoreSweeper,
)
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from ..utils.utils import print_test_function_name
from ..utils import asserts
import datetime
import time
from rich import print
from controlplane.datastore.types.machine_info import MachineRegistrationInfo
from .metric_utils import (
    MetricType,
    add_measurement,
    get_measurements,
)

machine_id = "test-machine-id"


def test_sweeper(
    datastore: tuple[DatastoreConfig, DatastoreClient],
    machine_registration_info: MachineRegistrationInfo,
):
    """
    Test that the sweeper actor deletes old data points
    """
    print_test_function_name()
    datastore_config, client = datastore

    # Add 10 old data points and 10 recent ones
    now = datetime.datetime.now(datetime.timezone.utc)
    num_metrics = 10
    # old
    timestamps = [
        now - datetime.timedelta(seconds=(i + 1) * 120) for i in range(num_metrics)
    ]
    # recent
    timestamps.extend(
        [now - datetime.timedelta(seconds=i * 0.1) for i in range(num_metrics)]
    )
    for ind, ts in enumerate(timestamps):
        for metric_type in MetricType:
            add_measurement(metric_type, client, machine_id, ts, ind)

    # Confirm that we have 20 data points
    for metric_type in MetricType:
        current_data = get_measurements(metric_type, client, machine_id)
        asserts.list_size(current_data, num_metrics * 2)

    # Start the sweeper so it runs frequently and deletes the 10 old data points
    datastore_sweeper_config = DatastoreSweeperConfig(
        sweep_interval_secs=1,
        data_retention_secs=60,
        reap_machines_interval_secs=1,
        machine_no_heartbeat_reap_secs=3,
    )
    sweeper = DatastoreSweeper.start(
        datastore_sweeper_config=datastore_sweeper_config,
        datastore_config=datastore_config,
    )

    # Test CPU timeseries cleanup
    try:
        time.sleep(2)

        # Confirm that we now only have 10 data points
        for metric_type in MetricType:
            current_data = get_measurements(metric_type, client, machine_id)
            asserts.list_size(current_data, num_metrics)

        # Cleanup
        print("Sweeper metric cleanup test passed")
    except Exception as e:
        sweeper.stop()
        raise e

    # Test machine reaping
    try:
        client.add_or_update_machine_info(
            machine_id=machine_id, registration_info=machine_registration_info
        )
        asserts.list_size(client.get_machines(), 1)
        time.sleep(5)
        asserts.list_size(client.get_machines(), 0)

        print("Sweeper machine reaping test passed")
    finally:
        sweeper.stop()
