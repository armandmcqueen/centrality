import time

import streamlit as st
from common.sdks.controlplane.sdk import get_sdk
from centrality_controlplane_sdk import DataApi

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
def get_live_machines(_sdk: DataApi, epoch: int) -> list[str]:
    live_machines = [m.machine_id for m in _sdk.get_live_machines()]
    # TODO: Handle errors?
    return sorted(live_machines)


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_cpu_metrics(
    _sdk: DataApi, live_machines: list[str], epoch: int
) -> list[MachineOverviewCardContents]:
    """Use epoch as a cache key to force a refresh at some interval"""
    measurements = _sdk.get_latest_cpu_metrics(machine_ids=live_machines)
    # TODO: Handle errors?
    return [
        MachineOverviewCardContents(
            machine_id=m.machine_id, avg_cpu=sum(m.cpu_percents) / len(m.cpu_percents)
        )
        for m in sorted(measurements, key=lambda m: m.machine_id)
    ]


def gen_data(
    _sdk: DataApi, config: StreamlitUiConfig
) -> tuple[list[str], list[MachineOverviewCardContents]]:
    live_machines = get_live_machines(
        _sdk=_sdk,
        epoch=calculate_epoch(interval_ms=config.live_machine_interval_ms),
    )
    if len(live_machines) == 0:
        return [], []
    cpu_metrics = get_cpu_metrics(
        _sdk=_sdk,
        live_machines=live_machines,
        epoch=calculate_epoch(interval_ms=config.metric_interval_ms),
    )
    return live_machines, cpu_metrics


def main():
    config = load_config()
    header("Cluster Overview")
    control_plane_sdk = get_sdk(
        config=config.control_plane_sdk, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN
    )

    live_machines, cpu_metrics = gen_data(control_plane_sdk, config)

    num_machines = len(live_machines)
    _, col2, _, col4, _ = st.columns(5)

    gpu_count = LiveMachineCount(col2, "GPU", 0)  # noqa
    cpu_count = LiveMachineCount(col4, "CPU", num_machines)

    flexbox = UniformFlexbox(3, MachineOverviewCard, border=True)
    flexbox.set_initial_cards(contents=cpu_metrics)

    while True:
        new_live_machines, cpu_metrics = gen_data(control_plane_sdk, config)
        flexbox.update_cards(cpu_metrics)

        # Update the count if it has changed
        if num_machines != len(new_live_machines):
            num_machines = len(new_live_machines)
            cpu_count.update(num_machines)

        time.sleep(0.1)


main()
