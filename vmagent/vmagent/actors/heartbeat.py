from types import TracebackType
from typing import Optional

import conclib
import pykka

from common import constants
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from vmagent.config import VmAgentConfig


class SendHeartbeat(conclib.ActorMessage):
    pass


class HeartbeatSender(conclib.Actor):
    # Why is this an actor+ticker and not simply a Ticker? Primarily because the thread shutdown mechanism
    # relies on all actors receiving a shutdown message and cleaning up any child tickers. It's simpler if
    # there is never a Ticker without a parent actor.
    URN = constants.VM_AGENT_HEARTBEAT_SENDER_ACTOR

    def __init__(
            self,
            vm_agent_config: VmAgentConfig,
            control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk
        self.ticker: Optional[SendHeartbeatTicker] = None
        super().__init__(urn=self.URN)

    def on_start(self) -> None:
        self.ticker = SendHeartbeatTicker(self.actor_ref)
        self.ticker.start()

    def on_stop(self) -> None:
        self.ticker.stop()

    def on_failure(
        self,
        exception_type: Optional[type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.ticker.stop()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendHeartbeat):
            print("[HeartbeatSender] Sending heartbeat")
            self.control_plane_sdk.send_heartbeat(vm_id=self.vm_agent_config.vm_id)
            print("[HeartbeatSender] Heartbeat sent")
        else:
            raise conclib.errors.UnexpectedMessageError(message)


class SendHeartbeatTicker(conclib.Ticker):
    TICK_INTERVAL = constants.VM_HEARTBEAT_INTERVAL_SECS

    def __init__(self, heartbeat_sender_ref: pykka.ActorRef):
        self.heartbeat_sender_ref = heartbeat_sender_ref
        super().__init__(interval=self.TICK_INTERVAL)

    def execute(self):
        self.heartbeat_sender_ref.tell(SendHeartbeat())
