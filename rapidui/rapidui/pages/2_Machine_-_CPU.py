import time
import streamlit as st

from rapidui.library.flexbox import UniformFlexbox
from rapidui.header import header
from rapidui.library.utils import load_config, calculate_epoch
from rapidui.library.constants import TOKEN
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from rapidui.library.cpu_view import CpuCardContents, CpuCard


@st.cache_data
def get_cpu_metrics_for_vm(
    _sdk: ControlPlaneSdk, vm_id: str, epoch: int
) -> list[CpuCardContents]:
    """Use epoch as a cache key to force a refresh at some interval"""
    resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=[vm_id])
    # TODO: Handle errors?
    assert (
        len(measurements) == 1
    ), f"There should exactly 1 result, but there was {len(measurements)}."
    cpu_vals = measurements[0].cpu_percents
    return [
        CpuCardContents(cpu_id=ind, curr_cpu=cpu) for ind, cpu in enumerate(cpu_vals)
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
    vm_id = select_container.selectbox("Select Machine", live_vms, index=None)

    # If there are no live VMs, don't query for data
    if len(live_vms) == 0 or vm_id is None:
        return

    cpu_cards = get_cpu_metrics_for_vm(
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
