from centrality_controlplane_sdk import VmRegistrationInfo
from vmagent.machineinfo.real import get_real_machine_info
from vmagent.machineinfo.config import FakeMachineInfoConfig


def get_fake_machine_info(config: FakeMachineInfoConfig) -> VmRegistrationInfo:
    machine_info = get_real_machine_info()
    for field in VmRegistrationInfo.model_fields:
        if getattr(config, field) is not None:
            setattr(machine_info, field, getattr(config, field))
    if machine_info.num_gpus == 0:
        machine_info.gpu_type = None
        machine_info.gpu_memory_mb = None
        machine_info.nvidia_driver_version = None

    # TODO: Do we want to allow the number of GPUs to be > 0, while the type, memory,
    #  and driver version are None? That would have to be explicitly done by the user...

    return machine_info
