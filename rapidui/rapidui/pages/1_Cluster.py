import time

import streamlit as st
from common.sdks.controlplane.sdk import get_sdk
from centrality_controlplane_sdk import DataApi, MachineInfo

from rapidui.library.flexbox import UniformFlexbox
from rapidui.library.cluster_view import (
    MachineOverviewCard,
    MachineOverviewCardContents,
    LiveMachineCount,
)
from rapidui.header import header
from rapidui.library.utils import load_config, calculate_epoch
from rapidui.library.config import StreamlitUiConfig
from common import constants


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_live_machines(_sdk: DataApi, epoch: int) -> list[MachineInfo]:
    live_machines = _sdk.get_live_machines()
    # TODO: Handle errors?
    return sorted(live_machines, key=lambda m: m.machine_id)


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_cpu_metrics(
    _sdk: DataApi, live_machines: list[str], epoch: int
) -> list[tuple[str, float]]:
    """Use epoch as a cache key to force a refresh at some interval"""
    measurements = _sdk.get_latest_cpu_metrics(machine_ids=live_machines)
    # TODO: Handle errors?
    return [
        (m.machine_id, sum(m.cpu_percents) / len(m.cpu_percents))
        for m in sorted(measurements, key=lambda m: m.machine_id)
    ]


def get_data(
    _sdk: DataApi, config: StreamlitUiConfig
) -> tuple[list[MachineInfo], list[MachineOverviewCardContents]]:
    live_machines = get_live_machines(
        _sdk=_sdk,
        epoch=calculate_epoch(interval_ms=config.live_machine_interval_ms),
    )
    if len(live_machines) == 0:
        return [], []
    cpu_metrics = get_cpu_metrics(
        _sdk=_sdk,
        live_machines=[m.machine_id for m in live_machines],
        epoch=calculate_epoch(interval_ms=config.metric_interval_ms),
    )
    avg_cpu_map = {machine_id: avg_cpu for machine_id, avg_cpu in cpu_metrics}
    card_contents = [
        MachineOverviewCardContents(
            machine_id=machine.machine_id,
            avg_cpu=avg_cpu_map[machine.machine_id],
            is_gpu=machine.num_gpus > 0,
        )
        for machine in live_machines
    ]
    return live_machines, card_contents


def main():
    config = load_config()
    header("Cluster Overview")
    control_plane_sdk = get_sdk(
        config=config.control_plane_sdk, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )
    live_machines, cpu_metrics = get_data(control_plane_sdk, config)
    cpu_machine = [m for m in live_machines if m.num_gpus == 0]
    gpu_machine = [m for m in live_machines if m.num_gpus > 0]
    _, col2, _, col4, _ = st.columns(5)

    gpu_count = LiveMachineCount(col2, "GPU", len(gpu_machine))
    cpu_count = LiveMachineCount(col4, "CPU", len(cpu_machine))

    flexbox = UniformFlexbox(3, MachineOverviewCard, border=True)
    flexbox.set_initial_cards(contents=cpu_metrics)

    while True:
        new_live_machines, cpu_metrics = get_data(control_plane_sdk, config)
        cpu_machine = [m for m in new_live_machines if m.num_gpus == 0]
        gpu_machine = [m for m in new_live_machines if m.num_gpus > 0]

        flexbox.update_cards(cpu_metrics)
        cpu_count.update(len(cpu_machine))
        gpu_count.update(len(gpu_machine))

        time.sleep(0.1)


main()
