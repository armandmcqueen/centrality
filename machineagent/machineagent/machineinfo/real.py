import psutil
import socket
from machineagent.machineinfo.cpu import get_num_cpus, get_cpu_description
from machineagent.machineinfo.gpu import get_nvidia_gpu_info
from centrality_controlplane_sdk import MachineRegistrationInfo


def get_host_memory_mb() -> int:
    """Returns host memory in MiB"""
    return int(psutil.virtual_memory().total / 1024 / 1024)


def get_hostname() -> str:
    """Returns hostname"""
    return socket.gethostname()


def get_real_machine_info() -> MachineRegistrationInfo:
    num_gpus, gpu_type, gpu_memory_mb, nvidia_driver_version = get_nvidia_gpu_info()
    num_cpus = get_num_cpus()
    cpu_description = get_cpu_description()
    host_memory_mb = get_host_memory_mb()
    hostname = get_hostname()
    return MachineRegistrationInfo(
        num_cpus=num_cpus,
        cpu_description=cpu_description,
        host_memory_mb=host_memory_mb,
        num_gpus=num_gpus,
        gpu_type=gpu_type,
        gpu_memory_mb=gpu_memory_mb,
        nvidia_driver_version=nvidia_driver_version,
        hostname=hostname,
    )
