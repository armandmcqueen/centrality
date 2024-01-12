from machineagent.machineinfo.config import MachineInfoConfig
from machineagent.machineinfo.real import get_real_machine_info
from machineagent.machineinfo.fake import get_fake_machine_info
from centrality_controlplane_sdk import MachineRegistrationInfo


def get_machine_info(config: MachineInfoConfig) -> MachineRegistrationInfo:
    if config.use_fake:
        return get_fake_machine_info(config.fake)
    else:
        return get_real_machine_info()
