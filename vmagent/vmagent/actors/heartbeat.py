import conclib

from common import constants
from common.sdks.controlplane.handwritten.sdk import ControlPlaneSdk
from vmagent.config import VmAgentConfig


class SendHeartbeat(conclib.ActorMessage):
    pass


class HeartbeatSender(conclib.PeriodicActor):
    URN = constants.VM_AGENT_HEARTBEAT_SENDER_ACTOR
    TICKS = {
        SendHeartbeat: constants.VM_HEARTBEAT_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: ControlPlaneSdk,
    ):
        self.vm_agent_config = vm_agent_config
        self.control_plane_sdk = control_plane_sdk
        super().__init__()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendHeartbeat):
            # print("💌 HeartbeatSender - sending heartbeat")  # TODO: Readd this once we have leveled logging
            try:
                self.control_plane_sdk.send_heartbeat(vm_id=self.vm_agent_config.vm_id)
            except Exception as e:
                print(f"🚨 HeartbeatSender - failed to send heartbeat: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
