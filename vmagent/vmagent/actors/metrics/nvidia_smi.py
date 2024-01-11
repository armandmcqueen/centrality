import conclib
from common import constants
from vmagent.config import VmAgentConfig
from vmagent.actors.metrics.samplers.nvidia_smi import NvidiaSmiSampler
from centrality_controlplane_sdk import DataApi, NvidiaSmiMeasurement
from datetime import datetime, timezone
import subprocess


output_example = """\
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA A100-SXM4-40GB          On  | 00000000:06:00.0 Off |                    0 |
| N/A   35C    P0              44W / 400W |      4MiB / 40960MiB |      0%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
"""


class SendNvidiaSmiMetric(conclib.ActorMessage):
    pass


class NvidiaSmiMetricCollector(conclib.PeriodicActor):
    URN = constants.VM_AGENT_NVIDIA_SMI_METRIC_COLLECTOR_ACTOR
    TICKS = {
        SendNvidiaSmiMetric: constants.VM_AGENT_METRIC_NVIDIA_SMI_INTERVAL_SECS,
    }

    def __init__(
        self,
        vm_agent_config: VmAgentConfig,
        control_plane_sdk: DataApi,
    ):
        self.vm_agent_config = vm_agent_config
        self.config = self.vm_agent_config.metrics.nvidia_smi
        self.control_plane_sdk = control_plane_sdk
        self.sampler = NvidiaSmiSampler()

        self.nvidia_smi_available = True
        try:
            subprocess.check_call("nvidia-smi", shell=True)
        except Exception:
            self.nvidia_smi_available = False

        self.nvidia_smi_pid = None

        super().__init__()

    def on_start(self) -> None:
        if self.nvidia_smi_available:
            try:
                subprocess.check_call("nvidia-smi -pm 1", shell=True)
            except Exception:
                print("❗️ Failed to enable persistence mode for nvidia-smi. Non-fatal")
                pass
        super().on_start()

    def send_nvidia_smi_metric(self) -> None:
        if self.config.use_fake:
            output = output_example
        else:
            if not self.nvidia_smi_available:
                return
            output = self.sampler.sample()
        measurement = NvidiaSmiMeasurement(
            vm_id=self.vm_agent_config.vm_id,
            ts=datetime.now(timezone.utc),
            output=output,
        )
        self.control_plane_sdk.put_nvidia_smi_metric(measurement)

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SendNvidiaSmiMetric):
            try:
                self.send_nvidia_smi_metric()
            except Exception as e:
                print(f"🚨 {self.__class__.__name__} - failed to send metric: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
