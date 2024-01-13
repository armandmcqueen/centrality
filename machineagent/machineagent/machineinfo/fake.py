from centrality_controlplane_sdk import MachineRegistrationInfo
from machineagent.machineinfo.real import get_real_machine_info
from machineagent.machineinfo.config import FakeMachineInfoConfig


def get_fake_machine_info(config: FakeMachineInfoConfig) -> MachineRegistrationInfo:
    """
    Get fake machine info by getting the real machine info and overriding the fields.

    If the config field is None, then the real machine info value is used.
    """
    machine_info = get_real_machine_info()
    for field in MachineRegistrationInfo.model_fields:
        if getattr(config, field) is not None:
            setattr(machine_info, field, getattr(config, field))
    if machine_info.num_gpus == 0:
        machine_info.gpu_type = None
        machine_info.gpu_memory_mb = None
        machine_info.nvidia_driver_version = None

    return machine_info
