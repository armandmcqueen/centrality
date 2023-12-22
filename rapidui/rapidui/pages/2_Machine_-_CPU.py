import time
import random
import streamlit as st

from rapidui.lib.cpu_view import CpuCard, CpuCardContents
from rapidui.lib.flexbox import UniformFlexbox
from rapidui.header import header
from rapidui.lib.utils import load_config, calculate_epoch
from rapidui.lib.constants import TOKEN
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from rapidui.lib.cpu_view import CpuCardContents, CpuCard


@st.cache_data
def get_cpu_metrics_for_vm(
        _sdk: ControlPlaneSdk,
        vm_id: str,
        epoch: int
) -> list[CpuCardContents]:
    """Use epoch as a cache key to force a refresh at some interval"""
    resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=[vm_id])
    # TODO: Handle errors?
    assert len(measurements) in (0, 1), "There should only be 1 or zero results."
    if len(measurements) == 0:
        # TODO: What do we want to do here? This should never happen
        return []
    cpu_vals = measurements[0].cpu_percents
    return [
        CpuCardContents(ind, m)
        for ind, m in enumerate(cpu_vals)
    ]

@st.cache_data
def get_live_vms(_sdk: ControlPlaneSdk, epoch: int) -> list[str]:
    resp, live_vms = _sdk.get_live_vms()
    # TODO: Handle errors?
    return sorted(live_vms)


def main():
    config = load_config()
    control_plane_sdk = ControlPlaneSdk(config=config.control_plane_sdk, token=TOKEN)
    header("Machine CPUs", disable_card_fill=True)


    live_vms = get_live_vms(
        _sdk=control_plane_sdk,
        epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms),
    )

    _, select_container, _ = st.columns(3)
    vm_id = select_container.selectbox("Select Machine", live_vms, index=0)
    st.divider()
    cpu_cards= get_cpu_metrics_for_vm(
        _sdk=control_plane_sdk,
        vm_id=vm_id,
        epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms),
    )


    flexbox = UniformFlexbox(4, CpuCard, border=False)
    flexbox.set_initial_cards(cpu_cards)

    while True:
        cpu_cards = get_cpu_metrics_for_vm(
            _sdk=control_plane_sdk,
            vm_id=vm_id,
            epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms),
        )
        flexbox.update_cards(cpu_cards)
        time.sleep(0.1)


main()