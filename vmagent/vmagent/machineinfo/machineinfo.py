from vmagent.machineinfo.config import MachineInfoConfig
from vmagent.machineinfo.real import get_real_machine_info
from vmagent.machineinfo.fake import get_fake_machine_info
from centrality_controlplane_sdk import VmRegistrationInfo


def get_machine_info(config: MachineInfoConfig) -> VmRegistrationInfo:
    if config.use_fake:
        return get_fake_machine_info(config.fake)
    else:
        return get_real_machine_info()
