import psutil

"""
num_cpus: StrictInt
cpu_description: StrictStr
host_memory_mb: StrictInt
num_gpus: StrictInt
gpu_type: Optional[StrictStr]
gpu_memory_mb: Optional[StrictInt]
hostname: StrictStr
"""


def get_num_cpus() -> int:
    """Returns logical CPU count"""
    return psutil.cpu_count()


def get_cpu_description() -> str:
    """Returns CPU description, such as "Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz" """
