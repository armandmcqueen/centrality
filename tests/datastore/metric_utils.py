from controlplane.datastore.client import DatastoreClient
from ..utils import asserts

from ..utils.parameterized_metrics_sdk import MetricType


def add_measurement(
    metric_type: MetricType,
    client,
    machine_id: str,
    ts,
    ind,
):
    if metric_type == MetricType.CPU:
        client.add_cpu_measurement(
            machine_id=machine_id,
            metrics=[ind, ind, ind, ind],
            ts=ts,
        )
    elif metric_type == MetricType.MEMORY:
        client.add_memory_measurement(
            machine_id=machine_id,
            metrics=[ind, ind],
            ts=ts,
        )

    elif metric_type == MetricType.NETWORK:
        client.add_network_throughput_measurement(
            machine_id=machine_id,
            metrics={"iface": [ind, ind], "total": [ind, ind]},
            ts=ts,
        )

    elif metric_type == MetricType.DISK_USAGE:
        client.add_disk_usage_measurement(
            machine_id=machine_id,
            metrics={"disk": [ind, ind], "total": [ind, ind]},
            ts=ts,
        )
    elif metric_type == MetricType.DISK_IOPS:
        client.add_disk_iops_measurement(
            machine_id=machine_id,
            metrics={"disk": ind},
            ts=ts,
        )
    elif metric_type == MetricType.DISK_THROUGHPUT:
        client.add_disk_throughput_measurement(
            machine_id=machine_id,
            metrics={"disk": [ind, ind]},
            ts=ts,
        )
    elif metric_type == MetricType.GPU_MEMORY:
        client.add_gpu_memory_measurement(
            machine_id=machine_id,
            metrics=[[ind, ind], [ind, ind]],
            ts=ts,
        )
    elif metric_type == MetricType.GPU_UTILIZATION:
        client.add_gpu_utilization_measurement(
            machine_id=machine_id,
            metrics=[ind, ind],
            ts=ts,
        )
    else:
        raise Exception("Unknown metric type")


def get_latest_measurement(
    metric_type: MetricType, client: DatastoreClient, machine_id: str
):
    if metric_type == MetricType.CPU:
        return client.get_latest_cpu_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.MEMORY:
        return client.get_latest_memory_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.NETWORK:
        return client.get_latest_network_throughput_measurements(
            machine_ids=[machine_id]
        )
    elif metric_type == MetricType.DISK_USAGE:
        return client.get_latest_disk_usage_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.DISK_IOPS:
        return client.get_latest_disk_iops_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return client.get_latest_disk_throughput_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.GPU_MEMORY:
        return client.get_latest_gpu_memory_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.GPU_UTILIZATION:
        return client.get_latest_gpu_utilization_measurements(machine_ids=[machine_id])
    else:
        raise Exception("Unknown metric type")


def get_measurements(metric_type: MetricType, client, machine_id: str):
    if metric_type == MetricType.CPU:
        return client.get_cpu_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.MEMORY:
        return client.get_memory_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.NETWORK:
        return client.get_network_throughput_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.DISK_USAGE:
        return client.get_disk_usage_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.DISK_IOPS:
        return client.get_disk_iops_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return client.get_disk_throughput_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.GPU_MEMORY:
        return client.get_gpu_memory_measurements(machine_ids=[machine_id])
    elif metric_type == MetricType.GPU_UTILIZATION:
        return client.get_gpu_utilization_measurements(machine_ids=[machine_id])
    else:
        raise Exception("Unknown metric type")


def delete_old_measurements(
    metric_type: MetricType, client, machine_id: str, oldest_ts_to_keep
):
    if metric_type == MetricType.CPU:
        client.delete_old_cpu_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.MEMORY:
        client.delete_old_memory_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.NETWORK:
        client.delete_old_network_throughput_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_USAGE:
        client.delete_old_disk_usage_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_IOPS:
        client.delete_old_disk_iops_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.DISK_THROUGHPUT:
        client.delete_old_disk_throughput_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.GPU_MEMORY:
        client.delete_old_gpu_memory_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    elif metric_type == MetricType.GPU_UTILIZATION:
        client.delete_old_gpu_utilization_measurements(
            machine_ids=[machine_id], oldest_ts_to_keep=oldest_ts_to_keep
        )
    else:
        raise Exception("Unknown metric type")


def check_expected_measurement_value(metric_type, val, ind):
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
