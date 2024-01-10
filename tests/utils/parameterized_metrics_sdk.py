from enum import Enum
from centrality_controlplane_sdk import (
    DataApi,
    CpuMeasurement,
    MemoryMeasurement,
    NetworkThroughputMeasurement,
    DiskUsageMeasurement,
    DiskIopsMeasurement,
    DiskThroughputMeasurement,
    GpuMemoryMeasurement,
    GpuUtilizationMeasurement,
)
from typing import cast


class MetricType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    DISK_USAGE = "disk_usage"
    DISK_IOPS = "disk_io"
    DISK_THROUGHPUT = "disk_throughput"
    GPU_MEMORY = "gpu_memory"
    GPU_UTILIZATION = "gpu_utilization"


def get_latest_metric_sdk(metric_type: MetricType, sdk: DataApi, vm_ids: list[str]):
    if metric_type == MetricType.CPU:
        return sdk.get_latest_cpu_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.MEMORY:
        return sdk.get_latest_memory_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.NETWORK:
        return sdk.get_latest_network_throughput_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.DISK_USAGE:
        return sdk.get_latest_disk_usage_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.DISK_IOPS:
        return sdk.get_latest_disk_iops_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.DISK_THROUGHPUT:
        return sdk.get_latest_disk_throughput_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.GPU_MEMORY:
        return sdk.get_latest_gpu_memory_metrics(vm_ids=vm_ids)
    elif metric_type == MetricType.GPU_UTILIZATION:
        return sdk.get_latest_gpu_utilization_metrics(vm_ids=vm_ids)
    else:
        raise Exception("Unknown metric type")


def validate_measurement_is_sane(metric_type: MetricType, measurement):
    if metric_type == MetricType.CPU:
        measurement = cast(CpuMeasurement, measurement)
        assert len(measurement.cpu_percents) > 0
    elif metric_type == MetricType.MEMORY:
        measurement = cast(MemoryMeasurement, measurement)
        assert measurement.free_memory_mb > 0
        assert measurement.total_memory_mb > 0
        assert measurement.free_memory_mb <= measurement.total_memory_mb
    elif metric_type == MetricType.NETWORK:
        measurement = cast(NetworkThroughputMeasurement, measurement)
        assert len(measurement.per_interface) > 0
        assert measurement.total.interface_name == "total"
    elif metric_type == MetricType.DISK_USAGE:
        measurement = cast(DiskUsageMeasurement, measurement)
        assert len(measurement.usage) > 0
    elif metric_type == MetricType.DISK_IOPS:
        measurement = cast(DiskIopsMeasurement, measurement)
        assert len(measurement.iops) > 0
    elif metric_type == MetricType.DISK_THROUGHPUT:
        measurement = cast(DiskThroughputMeasurement, measurement)
        assert len(measurement.throughput) > 0
    elif metric_type == MetricType.GPU_MEMORY:
        measurement = cast(GpuMemoryMeasurement, measurement)
        assert len(measurement.memory) > 0
    elif metric_type == MetricType.GPU_UTILIZATION:
        measurement = cast(GpuUtilizationMeasurement, measurement)
        assert len(measurement.gpu_percents) > 0
    else:
        raise Exception("Unknown metric type")
