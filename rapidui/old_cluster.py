import time
import streamlit as st
from common.config.config import CentralityConfig
from common.types.vmmetrics import CpuMeasurement
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig
from pydantic import Field

TOKEN = "dev"
# LOGO_SVG = (
#     "https://armandmcqueenpublic.blob.core.windows.net/centrality-public/logo-blue.svg"
# )


# class StreamlitUiConfig(CentralityConfig):
#     control_plane_sdk: ControlPlaneSdkConfig = Field(
#         default_factory=ControlPlaneSdkConfig
#     )
#     live_vm_interval_ms: int = 5000
#     cpu_metric_interval_ms: int = 200


# @st.cache_data
# def get_config() -> StreamlitUiConfig:
#     return StreamlitUiConfig()


# @st.cache_data
# def get_live_vms(_sdk: ControlPlaneSdk, epoch: int) -> list[str]:
#     resp, live_vms = _sdk.get_live_vms()
#     # TODO: Handle errors?
#     return sorted(live_vms)
#
#
# @st.cache_data
# def get_cpu_metrics(
#     _sdk: ControlPlaneSdk, live_vms: list[str], epoch: int
# ) -> list[CpuMeasurement]:
#     """Use epoch as a cache key to force a refresh at some interval"""
#     resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=live_vms)
#
#     # TODO: Handle errors?
#     return sorted(measurements, key=lambda m: m.vm_id)


# def calculate_epoch(interval_ms: int) -> int:
#     current_sec = int(time.time() * 1000)
#     return int(current_sec / interval_ms)

#
# class MachineCard:
#     def __init__(self, container, vm_id, avg_cpu):
#         self.container = container
#         self.vm_id = vm_id
#         self.title = container.empty()
#         self.title.write(f"{self.vm_id}")
#         self.progress = container.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")
#
#     def update_progress(self, avg_cpu):
#         self.progress.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")
#
#     def rewrite(self, vm_id, avg_cpu):
#         self.vm_id = vm_id
#         self.title.write(f"{self.vm_id}")
#         self.progress.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")
#
#     def empty(self):
#         self.container.empty()
#         self.title.empty()
#         self.progress.empty()

#
# class CardFlexbox:
#     def __init__(self, num_cols):
#         self.num_cols = num_cols
#         self.cols = st.columns(num_cols)
#         self.cards = []
#
#     def set_cards(self, measurements: list[CpuMeasurement]) -> None:
#         sorted_measurements = sorted(measurements, key=lambda m: m.vm_id)
#         assert (
#             len(self.cards) == 0
#         ), "Can't set cards if there are already cards. Use update_cards instead."
#         for ind, m in enumerate(sorted_measurements):
#             card_container = self.cols[ind % self.num_cols].container(border=True)
#             card = MachineCard(card_container, m.vm_id, m.avg_cpu_percent)
#             self.cards.append(card)
#
#     def update_cards(self, measurements: list[CpuMeasurement]) -> None:
#         """
#         Given a new set of measurements, update the cards to represent them. This will completely
#         rewrite the cards and add any new ones.
#
#         Note that if the number of cards decreases, there will be ghosts because we can't actually
#         truly delete a card - the border still shows up.
#         """
#         sorted_measurements = sorted(measurements, key=lambda m: m.vm_id)
#         rewrites = sorted_measurements[: len(self.cards)]
#         additions = sorted_measurements[len(self.cards) :]
#         for ind, measurement in enumerate(rewrites):
#             self.cards[ind].rewrite(measurement.vm_id, measurement.avg_cpu_percent)
#
#         if len(rewrites) < len(self.cards):
#             # Any cards with an index >= len(rewrites) need to be emptied
#             for card in self.cards[len(rewrites) :]:
#                 card.empty()
#
#         for ind, measurement in enumerate(additions):
#             real_ind = ind + len(rewrites)
#             card_container = self.cols[real_ind % self.num_cols].container(border=True)
#             card = MachineCard(
#                 card_container, measurement.vm_id, measurement.avg_cpu_percent
#             )
#             self.cards.append(card)
#
#     @property
#     def current_vm_ids(self) -> list[str]:
#         return [c.vm_id for c in self.cards]
#

def cluster_view():
    config = StreamlitUiConfig()
    control_plane_sdk = ControlPlaneSdk(config=config.control_plane_sdk, token=TOKEN)
    # container = st.container()
    # logo_style = "display: block; margin-left: 0; width: 34px; "
    # full_logo = f"""
    # <div style='display: flex'>
    #     <img src='{LOGO_SVG}' style='{logo_style}'>
    #     <p style='text-align: left; padding-top: 18px; padding-left: 10px; font-size: 15px;'>Centrality</p>
    # </div>
    # """
    # container.markdown(full_logo, unsafe_allow_html=True)
    # container.markdown("<h2 style='text-align: center;'>Centrality Demo Cluster</h1>", unsafe_allow_html=True)
    # st.divider()

    # Get initial data
    live_vms = get_live_vms(
        _sdk=control_plane_sdk,
        epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms),
    )
    cpu_metrics = get_cpu_metrics(
        _sdk=control_plane_sdk,
        live_vms=live_vms,
        epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms),
    )

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
        gen_cpu_count_container_markdown(len(live_vms)), unsafe_allow_html=True
    )

    flexbox = CardFlexbox(num_cols=3)
    flexbox.set_cards(cpu_metrics)

    while True:
        live_vms = get_live_vms(
            _sdk=control_plane_sdk,
            epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms),
        )
        cpu_metrics = get_cpu_metrics(
            _sdk=control_plane_sdk,
            live_vms=live_vms,
            epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms),
        )
        live_vms_changed = set(flexbox.current_vm_ids) != set(live_vms)
        if live_vms_changed:
            # TODO: Sad we can't actually delete cards. This will leave a ghost card.
            flexbox.update_cards(cpu_metrics)
            cpu_container.empty()
            cpu_container.markdown(
                gen_cpu_count_container_markdown(len(live_vms)), unsafe_allow_html=True
            )

        else:
            for card, m in zip(flexbox.cards, cpu_metrics):
                card.update_progress(m.avg_cpu_percent)

        time.sleep(0.1)


# st.set_page_config(
#     page_icon="https://armandmcqueenpublic.blob.core.windows.net/centrality-public/favicon.ico",
#     page_title="Demo Cluster | Centrality",
# )
# st.markdown(
#     r"""
#         <style>
#
#         @import url('https://rsms.me/inter/inter.css');
#
#         html, body, h2, h1, h3, p, span [class*="css"] {
#             font-family: 'Inter', sans-serif;
#         }
#
#         h2 {
#             font-weight: 400;
#             font-size: 1.8rem;
#         }
#
#         [data-testid="stHeader"] {
#                 visibility: hidden;
#             }
#         .block-container {
#             padding-top: 1rem;
#             max-width: 66rem;
#         }
#         [data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"] {
#             background-color: #233044;
#             background: #233044;
#         }
#
#         hr {
#             margin-top: 1em;
#         }
#         </style>
#         """,
#     unsafe_allow_html=True,
# )
cluster_view()
