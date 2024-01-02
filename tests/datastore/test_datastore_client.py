from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient

from common import constants
import datetime


def test_tokens(datastore: tuple[DatastoreConfig, DatastoreClient]):
    config, client = datastore
    client.reset_db()

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


def test_cpu_measurements(datastore: tuple[DatastoreConfig, DatastoreClient]):
    VM_ID = "examplevm"
    config, client = datastore
    client.reset_db()

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


# TODO: Test with multiple VM IDs in the db
# TODO: Test filtering by timestamp