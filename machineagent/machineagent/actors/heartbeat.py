import conclib

from common import constants
from centrality_controlplane_sdk import DataApi
from machineagent.config import MachineAgentConfig


class SendHeartbeat(conclib.ActorMessage):
    pass


class HeartbeatSender(conclib.PeriodicActor):
    URN = constants.VM_AGENT_HEARTBEAT_SENDER_ACTOR
    TICKS = {
        SendHeartbeat: constants.VM_HEARTBEAT_INTERVAL_SECS,
    }

    def __init__(
        self,
        machine_agent_config: MachineAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.machine_agent_config = machine_agent_config
        self.control_plane_sdk = control_plane_sdk
        super().__init__()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendHeartbeat):
            # print("💌 HeartbeatSender - sending heartbeat")  # TODO: Readd this once we have leveled logging
            try:
                self.control_plane_sdk.report_machine_heartbeat(
                    machine_id=self.machine_agent_config.machine_id
                )
            except Exception as e:
                print(f"🚨 HeartbeatSender - failed to send heartbeat: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
