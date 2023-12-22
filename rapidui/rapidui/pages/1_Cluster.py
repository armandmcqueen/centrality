import time

import streamlit as st
from common.types.vmmetrics import CpuMeasurement
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk

from rapidui.lib.flexbox import UniformFlexbox
from rapidui.lib.cluster_view import MachineOverviewCard, MachineOverviewCardContents
from rapidui.header import header
from rapidui.lib.utils import load_config, calculate_epoch
from rapidui.lib.config import StreamlitUiConfig

TOKEN = "dev"


# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_live_vms(_sdk: ControlPlaneSdk, epoch: int) -> list[str]:
    resp, live_vms = _sdk.get_live_vms()
    # TODO: Handle errors?
    return sorted(live_vms)

# Use caching with epochs to only refresh data at some interval
@st.cache_data
def get_cpu_metrics(
        _sdk: ControlPlaneSdk,
        live_vms: list[str],
        epoch: int
) -> list[MachineOverviewCardContents]:
    """Use epoch as a cache key to force a refresh at some interval"""
    resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=live_vms)
    # TODO: Handle errors?
    return [
        MachineOverviewCardContents(vm_id=m.vm_id, avg_cpu=m.avg_cpu_percent)
        for m in sorted(measurements, key=lambda m: m.vm_id)
    ]


def gen_data(control_plane_sdk: ControlPlaneSdk, config: StreamlitUiConfig) -> tuple[list[str], list[MachineOverviewCardContents]]:
    live_vms = get_live_vms(
        _sdk=control_plane_sdk,
        epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms),
    )
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

    live_vms, cpu_metrics = gen_data(control_plane_sdk, config)

    ##############################################################################
    # TODO: Abstract this
    num_vms = len(live_vms)
    col1, gpu_count_container, col3, cpu_count_container, col5 = st.columns(5)
    gpu_count_container.markdown(
        f"""
                <div style='background-color: #1B2635'>
                    <h3 style='text-align: center;'>0</h3>
                    <p style='text-align: center;'>GPU Machines</p>
                    <br/>
                <div>
                """,
        unsafe_allow_html=True,
    )

    def gen_cpu_count_container_markdown(num_live_vms):
        return f"""
                    <div style='background-color: #1B2635'>
                        <h3 style='text-align: center;'>{num_live_vms}</h3>
                        <p style='text-align: center;'>CPU Machines</p>
                        <br/>
                    <div>
                    """

    cpu_container = cpu_count_container.empty()
    cpu_container.markdown(
        gen_cpu_count_container_markdown(num_vms), unsafe_allow_html=True
    )
    ##############################################################################

    flexbox = UniformFlexbox(3, MachineOverviewCard, border=True)
    flexbox.set_initial_cards(contents=cpu_metrics)

    while True:
        live_vms, cpu_metrics = gen_data(control_plane_sdk, config)
        flexbox.update_cards(cpu_metrics)

        ##############################################################################
        # TODO: Abstract this
        live_vms_changed = len(live_vms) != num_vms
        if live_vms_changed:
            cpu_container.empty()
            cpu_container.markdown(
                gen_cpu_count_container_markdown(len(live_vms)), unsafe_allow_html=True
            )
            num_vms = len(live_vms)
        ##############################################################################

        time.sleep(0.1)


main()
