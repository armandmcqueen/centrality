import time
import streamlit as st


from rapidui.library.flexbox import UniformFlexbox
from rapidui.header import header
from rapidui.library.utils import load_config, calculate_epoch
from common.sdks.controlplane.sdk import get_sdk
from common import constants
from centrality_controlplane_sdk import DataApi
from rapidui.library.flexbox import CardContents, BaseCard
from rapidui.library.cpu_view import CpuCardContents, CpuCard
from rapidui.library.gpu_util_view import GpuUtilCardContents, GpuUtilCard
from rapidui.library.gpu_mem_view import GpuMemCardContents, GpuMemCard
from rapidui.library.mem_view import MemCardContents, MemCard
from rapidui.library.disk_usage_view import DiskUsageCardContents, DiskUsageCard
from rapidui.library.disk_io_view import DiskIoCardContents, DiskIoCard
from rapidui.library.net_view import NetThroughputCardContents, NetThroughputCard
from rapidui.library.nvidia_smi_view import NvidiaSmiCardContents, NvidiaSmiCard
from rapidui.library.machine_info_view import MachineInfoCardContents, MachineInfoCard
from enum import Enum


class MetricType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    DISK_USAGE = "disk_usage"
    DISK_IO = "disk_io"
    GPU_MEMORY = "gpu_memory"
    GPU_UTILIZATION = "gpu_utilization"
    NVIDIA_SMI = "nvidia_smi"
    MACHINE_INFO = "machine_info"


UseBorder = bool


@st.cache_data
def get_metrics_for_machine(
    _sdk: DataApi, machine_id: str, metric_type: MetricType, epoch: int
) -> tuple[type[BaseCard], list[CardContents], UseBorder]:
    """Use epoch as a cache key to force a refresh at some interval"""
    if metric_type == MetricType.CPU:
        measurements = _sdk.get_latest_cpu_metrics(machine_ids=[machine_id])
        # TODO: Handle errors?
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        cpu_vals = measurements[machine_id].cpu_percents
        return (
            CpuCard,
            [
                CpuCardContents(cpu_id=ind, curr_cpu=cpu)
                for ind, cpu in enumerate(cpu_vals)
            ],
            False,
        )
    elif metric_type == MetricType.GPU_UTILIZATION:
        measurements = _sdk.get_latest_gpu_utilization_metrics(machine_ids=[machine_id])
        if len(measurements) == 0:
            return GpuUtilCard, [], False
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        gpu_vals = measurements[machine_id].gpu_percents
        return (
            GpuUtilCard,
            [
                GpuUtilCardContents(gpu_id=ind, curr_gpu=gpu)
                for ind, gpu in enumerate(gpu_vals)
            ],
            False,
        )
    elif metric_type == MetricType.GPU_MEMORY:
        measurements = _sdk.get_latest_gpu_memory_metrics(machine_ids=[machine_id])
        if len(measurements.keys()) == 0:
            return GpuMemCard, [], True
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        per_cpu_mem = measurements[machine_id].memory
        return (
            GpuMemCard,
            [
                GpuMemCardContents(
                    gpu_id=ind, used_mem=gpu.used_mb, total_mem=gpu.total_mb
                )
                for ind, gpu in enumerate(per_cpu_mem)
            ],
            True,
        )
    elif metric_type == MetricType.MEMORY:
        measurements = _sdk.get_latest_memory_metrics(machine_ids=[machine_id])
        if len(measurements.keys()) == 0:
            return MemCard, [], True
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        free_mb = measurements[machine_id].free_memory_mb
        total_mb = measurements[machine_id].total_memory_mb
        return MemCard, [MemCardContents(free_mem=free_mb, total_mem=total_mb)], True
    elif metric_type == MetricType.DISK_USAGE:
        measurements = _sdk.get_latest_disk_usage_metrics(machine_ids=[machine_id])
        if len(measurements.keys()) == 0:
            return DiskUsageCard, [], True
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        return (
            DiskUsageCard,
            [
                DiskUsageCardContents(
                    disk_name=disk.disk_name,
                    used_mb=disk.used_mb,
                    total_mb=disk.total_mb,
                )
                for disk_name, disk in measurements[machine_id].usage.items()
            ],
            True,
        )
    elif metric_type == MetricType.DISK_IO:
        iops_measurements = _sdk.get_latest_disk_iops_metrics(machine_ids=[machine_id])
        throughput_measurements = _sdk.get_latest_disk_throughput_metrics(
            machine_ids=[machine_id]
        )
        assert len(iops_measurements.keys()) == len(
            throughput_measurements
        ), "There should be the same number of iops and throughput measurements"
        if len(iops_measurements.keys()) == 0:
            return DiskUsageCard, [], True
        assert (
            len(iops_measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(iops_measurements)}."

        card_contents = []
        throughput_map = {
            t.disk_name: t for t in throughput_measurements[machine_id].throughput
        }
        for disk_name, iop in iops_measurements[machine_id].iops.items():
            throughput = throughput_map[iop.disk_name]
            card_contents.append(
                DiskIoCardContents(
                    disk_name=iop.disk_name,
                    write_mbps=throughput.write_mbps,
                    read_mbps=throughput.read_mbps,
                    iops=iop.iops,
                )
            )
        return DiskIoCard, card_contents, True
    elif metric_type == MetricType.NETWORK:
        measurements = _sdk.get_latest_network_throughput_metrics(
            machine_ids=[machine_id]
        )
        print("MEASUREMENTS RETRIEVED!")
        print(measurements)
        if len(measurements.keys()) == 0:
            return NetThroughputCard, [], True
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        m = measurements[machine_id]
        per_interface = m.per_interface
        cards = []
        total_card = NetThroughputCardContents(
            interface_name=m.total.interface_name,
            sent_mbps=m.total.sent_mbps,
            recv_mbps=m.total.recv_mbps,
        )
        for interface_name, throughput in per_interface.items():
            card = NetThroughputCardContents(
                interface_name=throughput.interface_name,
                sent_mbps=throughput.sent_mbps,
                recv_mbps=throughput.recv_mbps,
            )
            cards.append(card)
        # sort cards and add total to the front
        cards = sorted(cards, key=lambda c: c.interface_name)
        cards.insert(0, total_card)
        return NetThroughputCard, cards, True
    elif metric_type == MetricType.NVIDIA_SMI:
        measurements = _sdk.get_latest_nvidia_smi_metrics(machine_ids=[machine_id])
        if len(measurements.keys()) == 0:
            return NvidiaSmiCard, [], True
        assert (
            len(measurements.keys()) == 1
        ), f"There should exactly 1 result, but there was {len(measurements)}."
        m = measurements[machine_id]

        card = [
            NvidiaSmiCardContents(
                output=m.output,
            )
        ]
        return NvidiaSmiCard, card, True
    elif metric_type == MetricType.MACHINE_INFO:
        machine_info = _sdk.get_machine(machine_id=machine_id)
        if machine_info is None:
            return MachineInfoCard, [], True
        card = [
            MachineInfoCardContents(
                machine_id=machine_info.machine_id,
                last_heartbeat_ts_dt=machine_info.last_heartbeat_ts,
                registration_ts_dt=machine_info.registration_ts,
                num_cpus=machine_info.num_cpus,
                cpu_description=machine_info.cpu_description,
                host_memory_mb=machine_info.host_memory_mb,
                num_gpus=machine_info.num_gpus,
                gpu_type=machine_info.gpu_type,
                gpu_memory_mb=machine_info.gpu_memory_mb,
                nvidia_driver_version=machine_info.nvidia_driver_version,
                hostname=machine_info.hostname,
            )
        ]
        return MachineInfoCard, card, False
    else:
        raise NotImplementedError(f"Metric type {metric_type} not implemented")


@st.cache_data
def get_live_machines(_sdk: DataApi, epoch: int) -> list[str]:
    live_machines = [m.machine_id for m in _sdk.get_live_machines()]
    # TODO: Handle errors?
    return sorted(live_machines)


def main():
    config = load_config()
    control_plane_sdk = get_sdk(
        config=config.control_plane_sdk, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    header("Machine Metrics", disable_card_fill=True)
    metric_type = st.sidebar.selectbox("Metric Type", list(MetricType))

    live_machines = get_live_machines(
        _sdk=control_plane_sdk,
        epoch=calculate_epoch(interval_ms=config.live_machine_interval_ms),
    )

    _, select_container, _ = st.columns(3)
    machine_id = select_container.selectbox("Select Machine", live_machines, index=None)

    # If there are no live machines, don't query for data
    if len(live_machines) == 0 or machine_id is None:
        return

    card_type, cards, use_border = get_metrics_for_machine(
        _sdk=control_plane_sdk,
        machine_id=machine_id,
        metric_type=metric_type,
        epoch=calculate_epoch(interval_ms=config.metric_interval_ms),
    )
    if len(cards) == 0:
        _, mid, _ = st.columns(3)
        mid.markdown("## No data available for this metric.")
        return

    num_cols = 4

    if len(cards) <= 8:
        num_cols = 2
    if len(cards) > 64:
        num_cols = 8

    if card_type in [NvidiaSmiCard, MachineInfoCard]:
        num_cols = 1

    flexbox = UniformFlexbox(num_cols=num_cols, card_type=card_type, border=use_border)
    flexbox.set_initial_cards(cards)

    while True:
        _, cards, _ = get_metrics_for_machine(
            _sdk=control_plane_sdk,
            machine_id=machine_id,
            metric_type=metric_type,
            epoch=calculate_epoch(interval_ms=config.metric_interval_ms),
        )
        flexbox.update_cards(cards)
        time.sleep(0.1)


main()
