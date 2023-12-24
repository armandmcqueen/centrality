import time

import streamlit as st
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk

from rapidui.library.flexbox import UniformFlexbox
from rapidui.library.cluster_view import (
    MachineOverviewCard,
    MachineOverviewCardContents,
    LiveMachineCount,
)
from rapidui.header import header
from rapidui.library.utils import load_config, calculate_epoch
from rapidui.library.config import StreamlitUiConfig
from rapidui.library.constants import TOKEN


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_live_vms(_sdk: ControlPlaneSdk, epoch: int) -> list[str]:
    resp, live_vms = _sdk.get_live_vms()
    # TODO: Handle errors?
    return sorted(live_vms)


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_cpu_metrics(
    _sdk: ControlPlaneSdk, live_vms: list[str], epoch: int
) -> list[MachineOverviewCardContents]:
    """Use epoch as a cache key to force a refresh at some interval"""
    resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=live_vms)
    # TODO: Handle errors?
    return [
        MachineOverviewCardContents(vm_id=m.vm_id, avg_cpu=m.avg_cpu_percent)
        for m in sorted(measurements, key=lambda m: m.vm_id)
    ]


def gen_data(
    control_plane_sdk: ControlPlaneSdk, config: StreamlitUiConfig
) -> tuple[list[str], list[MachineOverviewCardContents]]:
    live_vms = get_live_vms(
        _sdk=control_plane_sdk,
        epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms),
    )
    if len(live_vms) == 0:
        return [], []
    cpu_metrics = get_cpu_metrics(
        _sdk=control_plane_sdk,
        live_vms=live_vms,
        epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms),
    )
    return live_vms, cpu_metrics


def main():
    config = load_config()
    header("Cluster Overview")
    control_plane_sdk = ControlPlaneSdk(config=config.control_plane_sdk, token=TOKEN)

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
