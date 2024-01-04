from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from vmagent.machineinfo.machineinfo import get_machine_info
from vmagent.machineinfo.config import MachineInfoConfig
from ..utils.utils import print_test_function_name

from common import constants
import datetime
import time

VM_ID = "testvm"


def test_tokens(datastore: tuple[DatastoreConfig, DatastoreClient]):
    print_test_function_name()
    config, client = datastore

    # Validate that create a new token works
    user_token = client.new_token()
    token_val = user_token.token
    assert client.validate_token(
        constants.CONTROL_PLANE_SDK_DEV_TOKEN
    ), "Dev token was not found"
    assert client.validate_token(
        token_val
    ), f"Newly added token {token_val} was not found"
    tokens = client.get_tokens()
    expected_tokens = {constants.CONTROL_PLANE_SDK_DEV_TOKEN, token_val}
    actual_tokens = set([token.token for token in tokens])
    assert (
        actual_tokens == expected_tokens
    ), f"get_tokens expected {expected_tokens}, got {actual_tokens}"

    client.reset_db()
    assert client.validate_token(
        constants.CONTROL_PLANE_SDK_DEV_TOKEN
    ), "After DB reset, dev token was not found"
    assert not client.validate_token(
        token_val
    ), "After DB reset, previously created token was found"

    # TODO: Add code to delete tokens and test it


def test_vm_liveness(datastore: tuple[DatastoreConfig, DatastoreClient]):
    """Test that VM list, heartbeat, and removal works"""

    print_test_function_name()
    config, client = datastore

    # Test that initial state is correct
    live_vms = client.get_live_vms(constants.VM_NO_HEARTBEAT_LIMBO_SECS)
    assert len(live_vms) == 0, f"Expected there to be no live VMs, but got {live_vms}"

    # Test addition and forced removal
    machine_info_config = MachineInfoConfig(use_fake=True)
    client.register_vm(
        vm_id=VM_ID, registration_info=get_machine_info(machine_info_config)
    )
    client.report_heartbeat(VM_ID)
    live_vms = client.get_live_vms(constants.VM_NO_HEARTBEAT_LIMBO_SECS)
    assert live_vms == [VM_ID], f"Expected live vms to be {[VM_ID]}, but got {live_vms}"
    client.report_vm_death(VM_ID)
    live_vms = client.get_live_vms(constants.VM_NO_HEARTBEAT_LIMBO_SECS)
    assert len(live_vms) == 0, f"Expected there to be no live VMs, but got {live_vms}"

    # Test addition and timeout-based removal
    client.register_vm(
        vm_id=VM_ID, registration_info=get_machine_info(machine_info_config)
    )
    client.report_heartbeat(VM_ID)
    live_vms = client.get_live_vms(constants.VM_NO_HEARTBEAT_LIMBO_SECS)
    assert live_vms == [VM_ID], f"Expected live vms to be {[VM_ID]}, but got {live_vms}"
    time.sleep(3)
    live_vms = client.get_live_vms(liveness_threshold_secs=1)
    assert len(live_vms) == 0, f"Expected there to be no live VMs, but got {live_vms}"

    # TODO: This doesn't actually test the heartbeat


def test_cpu_measurements(datastore: tuple[DatastoreConfig, DatastoreClient]):
    # TODO: Test with multiple VM IDs in the db
    # TODO: Test filtering by timestamp
    print_test_function_name()
    config, client = datastore

    now = datetime.datetime.now(datetime.timezone.utc)
    # Create a timestamp for each of the last 5 seconds
    timestamps = [now - datetime.timedelta(seconds=i) for i in range(5)]

    for ind, ts in enumerate(timestamps):
        client.add_cpu_measurement(
            vm_id=VM_ID,
            cpu_percents=[ind, ind, ind, ind],
            ts=ts,
        )
        # TODO: Will this need a short sleep?

        # Check that the latest CPU measurement was updated correctly
        measurements = client.get_latest_cpu_measurements(vm_ids=[VM_ID])
        assert len(measurements) == 1, "Expected 1 measurement"
        measurement = measurements[0]
        assert measurement.vm_id == VM_ID, "VM ID mismatch"
        for i in range(4):
            assert measurement.cpu_percents[i] == ind, "CPU percent mismatch"

        # Check the entire timeseries
        measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
        assert (
            len(measurements) == ind + 1
        ), f"Expected {ind+1} measurement, but got {len(measurements)}"
        retrieved_timestamps = set([measurement.ts for measurement in measurements])
        assert retrieved_timestamps == set(
            timestamps[: ind + 1]
        ), f"Expected {timestamps[: ind + 1]}, got {retrieved_timestamps}"


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
            cpu_percents=[ind, ind, ind, ind],
            ts=ts,
        )

    # Check the entire timeseries
    measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    assert (
        len(measurements) == num_metrics
    ), f"Expected {num_metrics} measurement, but got {len(measurements)}"
    retrieved_timestamps = set([measurement.ts for measurement in measurements])
    all_timestamps = set(timestamps)
    assert (
        retrieved_timestamps == all_timestamps
    ), f"Expected {all_timestamps}, got {retrieved_timestamps}"

    # Delete all but the last 5 measurements
    cutoff_ts = timestamps[5] + datetime.timedelta(seconds=0.01)
    expected_timestamps = set(timestamps[:5])

    client.delete_old_cpu_measurements(oldest_ts_to_keep=cutoff_ts)
    measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    assert (
        len(measurements) == 5
    ), f"Expected 5 measurement, but got {len(measurements)}"
    retrieved_timestamps = set([measurement.ts for measurement in measurements])
    print(retrieved_timestamps)
    assert (
        retrieved_timestamps == expected_timestamps
    ), f"Expected {expected_timestamps}, got {retrieved_timestamps}"
