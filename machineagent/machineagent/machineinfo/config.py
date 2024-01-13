from common.config.config import CentralityConfig
from pydantic import Field
from typing import Optional


class FakeMachineInfoConfig(CentralityConfig):
    """
    Fake machine info for testing. Some sane defaults are provided. It is possible to mix and
    match real and fake data.

    If you want to use real machine info for any fields, set them to None. When using a yaml, there
    is a distinction between the field not being set (uses the default fake value) and the field being
    set to null (uses the real value). The logic behind this is to have an unset FakeMachineInfoConfig
    field produce a realistic look set of fake info, so that someone can simply set
    `use_fake_machine_info: true` in their config.

    If you want to use real data, you will need to set it explicitly to null, e.g.:
     ```yaml
    fake:
        # num_cpus: 8  # This unset field will use the default fake value of 8
        cpu_description: "Fake description"
    ```

    ```yaml
    fake:
        num_cpus: null  # This will use the real number of cpus
        cpu_description: "Fake description"
    ```


    """

    num_cpus: Optional[int] = 8
    cpu_description: Optional[str] = "Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz"
    host_memory_mb: Optional[int] = 16000
    num_gpus: Optional[int] = 8
    gpu_type: Optional[str] = "NVIDIA A100"
    gpu_memory_mb: Optional[int] = 60_000
    nvidia_driver_version: Optional[str] = "535.129.03"
    hostname: Optional[str] = "hostname"


class MachineInfoConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMachineInfoConfig = Field(default_factory=lambda: FakeMachineInfoConfig())
