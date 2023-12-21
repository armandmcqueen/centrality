import time
import streamlit as st
from common.config.config import CentralityConfig
from common.types.vmmetrics import CpuMeasurement
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from common.sdks.controlplane.handwritten.config import ControlPlaneSdkConfig
from pydantic import Field

TOKEN = "dev"


class StreamlitUiConfig(CentralityConfig):
    control_plane_sdk: ControlPlaneSdkConfig = Field(default_factory=ControlPlaneSdkConfig)
    live_vm_interval_ms: int = 5000
    cpu_metric_interval_ms: int = 200


@st.cache_data
def get_config() -> StreamlitUiConfig:
    return StreamlitUiConfig()


@st.cache_data
def get_live_vms(_sdk: ControlPlaneSdk, epoch: int) -> list[str]:
    resp, live_vms = _sdk.get_live_vms()
    # TODO: Handle errors?
    return sorted(live_vms)


@st.cache_data
def get_cpu_metrics(_sdk: ControlPlaneSdk, live_vms: list[str], epoch: int) -> list[CpuMeasurement]:
    """ Use epoch as a cache key to force a refresh at some interval """
    resp, measurements = _sdk.get_latest_cpu_measurements(vm_ids=live_vms)

    # TODO: Handle errors?
    return sorted(measurements, key=lambda m: m.vm_id)


def calculate_epoch(interval_ms: int) -> int:
    current_sec = int(time.time()*1000)
    return int(current_sec / interval_ms)


class MachineCard:
    def __init__(self, container, vm_id, avg_cpu):
        self.container = container
        self.vm_id = vm_id
        self.title = container.empty()
        self.title.write(f"**{self.vm_id}**")
        self.progress = container.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")

    def update_progress(self, avg_cpu):
        self.progress.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")

    def rewrite(self, vm_id, avg_cpu):
        self.vm_id = vm_id
        self.title.write(f"**{self.vm_id}**")
        self.progress.progress(avg_cpu / 100, text=f"{int(avg_cpu)}%")

    def empty(self):
        self.container.empty()
        self.title.empty()
        self.progress.empty()


class CardFlexbox:
    def __init__(self, num_cols):
        self.num_cols = num_cols
        self.cols = st.columns(num_cols)
        self.cards = []

    def set_cards(self, measurements: list[CpuMeasurement]) -> None:
        sorted_measurements = sorted(measurements, key=lambda m: m.vm_id)
        assert len(self.cards) == 0, "Can't set cards if there are already cards. Use update_cards instead."
        for ind, m in enumerate(sorted_measurements):
            card_container = self.cols[ind % self.num_cols].container(border=True)
            card = MachineCard(card_container, m.vm_id, m.avg_cpu_percent)
            self.cards.append(card)

    def update_cards(self, measurements: list[CpuMeasurement]) -> None:
        """
        Given a new set of measurements, update the cards to represent them. This will completely
        rewrite the cards and add any new ones.

        Note that if the number of cards decreases, there will be ghosts because we can't actually
        truly delete a card - the border still shows up.
        """
        sorted_measurements = sorted(measurements, key=lambda m: m.vm_id)
        rewrites = sorted_measurements[:len(self.cards)]
        additions = sorted_measurements[len(self.cards):]
        for ind, measurement in enumerate(rewrites):
            self.cards[ind].rewrite(measurement.vm_id, measurement.avg_cpu_percent)

        if len(rewrites) < len(self.cards):
            # Any cards with an index >= len(rewrites) need to be emptied
            for card in self.cards[len(rewrites):]:
                card.empty()

        for ind, measurement in enumerate(additions):
            real_ind = ind + len(rewrites)
            card_container = self.cols[real_ind % self.num_cols].container(border=True)
            card = MachineCard(card_container, measurement.vm_id, measurement.avg_cpu_percent)
            self.cards.append(card)

    @property
    def current_vm_ids(self) -> list[str]:
        return [c.vm_id for c in self.cards]


def cluster_view():
    config = StreamlitUiConfig()
    control_plane_sdk = ControlPlaneSdk(config=config.control_plane_sdk, token=TOKEN)

    st.write("# Centrality Demo Cluster - New")
    st.write("---")

    # Get initial data
    live_vms = get_live_vms(_sdk=control_plane_sdk, epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms))
    cpu_metrics = get_cpu_metrics(_sdk=control_plane_sdk, live_vms=live_vms,
                                  epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms))
    flexbox = CardFlexbox(num_cols=3)
    flexbox.set_cards(cpu_metrics)

    while True:
        live_vms = get_live_vms(_sdk=control_plane_sdk, epoch=calculate_epoch(interval_ms=config.live_vm_interval_ms))
        cpu_metrics = get_cpu_metrics(_sdk=control_plane_sdk, live_vms=live_vms,
                                      epoch=calculate_epoch(interval_ms=config.cpu_metric_interval_ms))
        live_vms_changed = set(flexbox.current_vm_ids) != set(live_vms)
        if live_vms_changed:
            # TODO: Sad we can't actually delete cards. This will leave a ghost card.
            flexbox.update_cards(cpu_metrics)

        else:
            for card, m in zip(flexbox.cards, cpu_metrics):
                card.update_progress(m.avg_cpu_percent)




st.markdown(
        r"""
        <style>
        [data-testid="stHeader"] {
                visibility: hidden;
            }
        .block-container {
            padding-top: 1rem;
            max-width: 66rem;
        }
        </style>
        """, unsafe_allow_html=True
    )
cluster_view()







