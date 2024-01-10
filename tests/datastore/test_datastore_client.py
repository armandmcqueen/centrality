from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from ..utils.utils import print_test_function_name
from ..utils import asserts
from controlplane.datastore.types.vmliveness import VmRegistrationInfo

from common import constants
import datetime
import time

VM_ID = "testvm"

# Short names to make the tests more readable
LIVETHRESH = constants.VM_NO_HEARTBEAT_LIMBO_SECS
TOKEN = constants.CONTROL_PLANE_SDK_DEV_TOKEN


def test_tokens(datastore: tuple[DatastoreConfig, DatastoreClient]):
    print_test_function_name()
    config, client = datastore

    # Validate that creating a new token works and that lists/get works
    user_token = client.new_token()
    new_token_val = user_token.token
    assert client.token_exists(TOKEN), "Dev token not found"
    assert client.token_exists(new_token_val), f"New token {new_token_val} not found"
    asserts.set_equality([t.token for t in client.get_tokens()], [TOKEN, new_token_val])

    # Validate that resetting the DB removes the token
    client.reset_db()
    assert client.token_exists(TOKEN), "After reset, dev token not found"
    assert not client.token_exists(
        new_token_val
    ), "After reset, previously created token still exists"

    # TODO: Add code to delete tokens and test it


def test_vm_addition_and_removal(
    datastore: tuple[DatastoreConfig, DatastoreClient],
    vm_registration_info: VmRegistrationInfo,
):
    """Test VM addition and removal"""
    print_test_function_name()
    config, client = datastore

    # Test that initial state is correct
    asserts.list_size(client.get_live_vms(LIVETHRESH), 0)

    # Test addition
    client.add_or_update_vm_info(vm_id=VM_ID, registration_info=vm_registration_info)
    asserts.set_equality(client.get_live_vms(LIVETHRESH), [VM_ID])

    # Test removal
    client.delete_vm_info(VM_ID)
    asserts.list_size(client.get_live_vms(LIVETHRESH), 0)


def test_vm_heartbeat_lifecycle(
    datastore: tuple[DatastoreConfig, DatastoreClient],
    vm_registration_info: VmRegistrationInfo,
):
    """Test the addition, liveness timeout removal, and heartbeat-based refresh of VMs"""
    print_test_function_name()
    config, client = datastore

    client.add_or_update_vm_info(vm_id=VM_ID, registration_info=vm_registration_info)
    asserts.set_equality(client.get_live_vms(LIVETHRESH), [VM_ID])

    # Wait so that the VM is considered dead with a small liveness_threshold_secs but not
    # with a larger one
    time.sleep(3)
    asserts.list_size(client.get_live_vms(liveness_threshold_secs=2), 0)
    asserts.list_size(client.get_live_vms(liveness_threshold_secs=LIVETHRESH), 1)

    # Test heartbeat adds it back to the live list
    client.update_vm_info_heartbeat_ts(VM_ID)
    asserts.list_size(client.get_live_vms(liveness_threshold_secs=2), 1)


# TODO: Parameterize this test across metrics
def test_cpu_measurements(datastore: tuple[DatastoreConfig, DatastoreClient]):
    # TODO: Test with multiple VM IDs in the db
    # TODO: Test filtering by timestamp
    print_test_function_name()
    config, client = datastore

    # Create a timestamp for each of the last 5 seconds
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamps = [now - datetime.timedelta(seconds=i) for i in range(5)]

    # Add a CPU measurement for each timestamp and validate that it was added correctly
    for ind, ts in enumerate(timestamps):
        client.add_cpu_measurement(
            vm_id=VM_ID,
            metrics=[ind, ind, ind, ind],
            ts=ts,
        )
        # TODO: Write every metric type

        # TODO: Check every metric type
        # Check that the latest CPU measurement was updated correctly
        measurements = client.get_latest_cpu_measurements(vm_ids=[VM_ID])
        asserts.list_size(measurements, 1)
        assert measurements[0].vm_id == VM_ID, "VM ID mismatch"
        assert measurements[0].ts == ts, "Timestamp mismatch"
        asserts.set_equality(measurements[0].cpu_percents, [ind, ind, ind, ind])

        # Check the entire timeseries
        # TODO: Check every metric type
        measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
        asserts.list_size(measurements, ind + 1)
        asserts.set_equality([m.ts for m in measurements], timestamps[: ind + 1])


def test_cpu_measurement_deletion(datastore: tuple[DatastoreConfig, DatastoreClient]):
    print_test_function_name()
    config, client = datastore

    # Addd some example data
    now = datetime.datetime.now(datetime.timezone.utc)
    num_metrics = 10
    timestamps = [now - datetime.timedelta(seconds=i) for i in range(num_metrics)]
    for ind, ts in enumerate(timestamps):
        client.add_cpu_measurement(
            vm_id=VM_ID,
            metrics=[ind, ind, ind, ind],
            ts=ts,
        )

    # Check the entire timeseries
    measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    asserts.list_size(measurements, num_metrics)
    asserts.set_equality([m.ts for m in measurements], timestamps)

    # Delete all but the last 5 measurements
    cutoff_ts = timestamps[5] + datetime.timedelta(seconds=0.01)
    client.delete_old_cpu_measurements(oldest_ts_to_keep=cutoff_ts)
    measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    asserts.list_size(measurements, 5)
    asserts.set_equality([m.ts for m in measurements], timestamps[:5])
