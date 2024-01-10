from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from ..utils.utils import print_test_function_name
from ..utils import asserts
from controlplane.datastore.types.vmliveness import VmRegistrationInfo

from common import constants
import datetime
import time
import pytest
from rich import print
from enum import Enum

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


class MetricType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    DISK_USAGE = "disk_usage"
    DISK_IOPS = "disk_io"
    DISK_THROUGHPUT = "disk_throughput"
    GPU_MEMORY = "gpu_memory"
    GPU_UTILIZATION = "gpu_utilization"


def add_measurement(
    metric_type: MetricType,
    client,
    vm_id: str,
    ts,
    ind,
):
    if metric_type == MetricType.CPU:
        client.add_cpu_measurement(
            vm_id=vm_id,
            metrics=[ind, ind, ind, ind],
            ts=ts,
        )
    elif metric_type == MetricType.MEMORY:
        client.add_memory_measurement(
            vm_id=vm_id,
            metrics=[ind, ind],
            ts=ts,
        )

    elif metric_type == MetricType.NETWORK:
        client.add_network_throughput_measurement(
            vm_id=vm_id,
            metrics={"iface": [ind, ind], "total": [ind, ind]},
            ts=ts,
        )

    elif metric_type == MetricType.DISK_USAGE:
        client.add_disk_usage_measurement(
            vm_id=vm_id,
            metrics={"disk": [ind, ind], "total": [ind, ind]},
            ts=ts,
        )
    elif metric_type == MetricType.DISK_IOPS:
        client.add_disk_iops_measurement(
            vm_id=vm_id,
            metrics={"disk": ind},
            ts=ts,
        )
    elif metric_type == MetricType.DISK_THROUGHPUT:
        client.add_disk_throughput_measurement(
            vm_id=vm_id,
            metrics={"disk": [ind, ind]},
            ts=ts,
        )
    elif metric_type == MetricType.GPU_MEMORY:
        client.add_gpu_memory_measurement(
            vm_id=vm_id,
            metrics=[[ind, ind], [ind, ind]],
            ts=ts,
        )
    elif metric_type == MetricType.GPU_UTILIZATION:
        client.add_gpu_utilization_measurement(
            vm_id=vm_id,
            metrics=[ind, ind],
            ts=ts,
        )
    else:
        raise Exception("Unknown metric type")


def get_latest_measurement(
    metric_type: MetricType, client: DatastoreClient, vm_id: str
):
    if metric_type == MetricType.CPU:
        return client.get_latest_cpu_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.MEMORY:
        return client.get_latest_memory_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.NETWORK:
        return client.get_latest_network_throughput_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_USAGE:
        return client.get_latest_disk_usage_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_IOPS:
        return client.get_latest_disk_iops_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return client.get_latest_disk_throughput_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.GPU_MEMORY:
        return client.get_latest_gpu_memory_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.GPU_UTILIZATION:
        return client.get_latest_gpu_utilization_measurements(vm_ids=[vm_id])
    else:
        raise Exception("Unknown metric type")


def get_measurements(metric_type: MetricType, client, vm_id: str):
    if metric_type == MetricType.CPU:
        return client.get_cpu_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.MEMORY:
        return client.get_memory_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.NETWORK:
        return client.get_network_throughput_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_USAGE:
        return client.get_disk_usage_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_IOPS:
        return client.get_disk_iops_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return client.get_disk_throughput_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.GPU_MEMORY:
        return client.get_gpu_memory_measurements(vm_ids=[vm_id])
    elif metric_type == MetricType.GPU_UTILIZATION:
        return client.get_gpu_utilization_measurements(vm_ids=[vm_id])
    else:
        raise Exception("Unknown metric type")


def delete_old_measurements(
    metric_type: MetricType, client, vm_id: str, oldest_ts_to_keep
):
    if metric_type == MetricType.CPU:
        return client.delete_old_cpu_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.MEMORY:
        return client.delete_old_memory_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.NETWORK:
        return client.delete_old_network_throughput_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_USAGE:
        return client.delete_old_disk_usage_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_IOPS:
        return client.delete_old_disk_iops_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return client.delete_old_disk_throughput_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.GPU_MEMORY:
        return client.delete_old_gpu_memory_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.GPU_UTILIZATION:
        return client.delete_old_gpu_utilization_measurements(
            vm_ids=[vm_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    else:
        raise Exception("Unknown metric type")


def check_expected_measurement_value(metric_type, val, ind):
    print(f"Checking metric type {metric_type}")
    print(val)
    if metric_type == MetricType.CPU:
        asserts.set_equality(val.cpu_percents, [ind, ind, ind, ind])
    elif metric_type == MetricType.MEMORY:
        asserts.matches(val.free_memory_mb, ind)
        asserts.matches(val.total_memory_mb, ind)
    elif metric_type == MetricType.NETWORK:
        asserts.matches(val.per_interface[0].sent_mbps, ind)
        asserts.matches(val.per_interface[0].recv_mbps, ind)
        asserts.matches(val.total.sent_mbps, ind)
        asserts.matches(val.total.recv_mbps, ind)
    elif metric_type == MetricType.DISK_USAGE:
        print(val.usage)
        asserts.matches(val.usage[0].used_mb, ind)
        asserts.matches(val.usage[0].total_mb, ind)
    elif metric_type == MetricType.DISK_IOPS:
        asserts.matches(val.iops[0].iops, ind)
    elif metric_type == MetricType.DISK_THROUGHPUT:
        asserts.matches(val.throughput[0].write_mbps, ind)
        asserts.matches(val.throughput[0].read_mbps, ind)
    elif metric_type == MetricType.GPU_MEMORY:
        asserts.matches(val.memory[0].used_mb, ind)
        asserts.matches(val.memory[0].total_mb, ind)
    elif metric_type == MetricType.GPU_UTILIZATION:
        asserts.set_equality(val.gpu_percents, [ind, ind])
    else:
        raise Exception("Unknown metric type")


# TODO: Parameterize this test across metrics
@pytest.mark.parametrize(
    "metric_type",
    [
        MetricType.CPU,
        MetricType.MEMORY,
        MetricType.NETWORK,
        MetricType.DISK_USAGE,
        MetricType.DISK_IOPS,
        MetricType.DISK_THROUGHPUT,
        MetricType.GPU_MEMORY,
        MetricType.GPU_UTILIZATION,
    ],
)
def test_metric_measurements(
    datastore: tuple[DatastoreConfig, DatastoreClient], metric_type: MetricType
):
    # TODO: Test with multiple VM IDs in the db
    # TODO: Test filtering by timestamp

    print_test_function_name()
    config, client = datastore

    # Create a timestamp for each of the last 5 seconds
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamps = [now - datetime.timedelta(seconds=i) for i in range(5)]

    # Add a CPU measurement for each timestamp and validate that it was added correctly
    for ind, ts in enumerate(timestamps):
        add_measurement(metric_type, client, VM_ID, ts, ind)

        # Check that the latest CPU measurement was updated correctly
        # measurements = client.get_latest_cpu_measurements(vm_ids=[VM_ID])
        measurements = get_latest_measurement(metric_type, client, VM_ID)
        asserts.list_size(measurements, 1)
        assert measurements[0].vm_id == VM_ID, "VM ID mismatch"
        assert measurements[0].ts == ts, "Timestamp mismatch"
        check_expected_measurement_value(metric_type, measurements[0], ind)
        print("....")
        # asserts.set_equality(measurements[0].cpu_percents, [ind, ind, ind, ind])

        # Check the entire timeseries
        # measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
        measurements = get_measurements(metric_type, client, VM_ID)
        asserts.list_size(measurements, ind + 1)
        asserts.set_equality([m.ts for m in measurements], timestamps[: ind + 1])


@pytest.mark.parametrize(
    "metric_type",
    [
        MetricType.CPU,
        MetricType.MEMORY,
        MetricType.NETWORK,
        MetricType.DISK_USAGE,
        MetricType.DISK_IOPS,
        MetricType.DISK_THROUGHPUT,
        MetricType.GPU_MEMORY,
        MetricType.GPU_UTILIZATION,
    ],
)
def test_measurement_deletion(
    datastore: tuple[DatastoreConfig, DatastoreClient], metric_type: MetricType
):
    print_test_function_name()
    config, client = datastore

    # Addd some example data
    now = datetime.datetime.now(datetime.timezone.utc)
    num_metrics = 10
    timestamps = [now - datetime.timedelta(seconds=i) for i in range(num_metrics)]
    for ind, ts in enumerate(timestamps):
        add_measurement(metric_type, client, VM_ID, ts, ind)

    # Check the entire timeseries
    measurements = get_measurements(metric_type, client, VM_ID)
    # measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    asserts.list_size(measurements, num_metrics)
    asserts.set_equality([m.ts for m in measurements], timestamps)

    # Delete all but the last 5 measurements
    cutoff_ts = timestamps[5] + datetime.timedelta(seconds=0.01)
    delete_old_measurements(metric_type, client, VM_ID, cutoff_ts)
    # client.delete_old_cpu_measurements(oldest_ts_to_keep=cutoff_ts)
    measurements = get_measurements(metric_type, client, VM_ID)
    # measurements = client.get_cpu_measurements(vm_ids=[VM_ID])
    asserts.list_size(measurements, 5)
    asserts.set_equality([m.ts for m in measurements], timestamps[:5])
