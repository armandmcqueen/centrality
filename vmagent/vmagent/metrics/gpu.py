import pynvml
from rich import print
from rich.live import Live
from vmagent.metrics.collector import MetricCollector

GpuUtil = float
GpuUtilList = list[GpuUtil]
GpuUsedMemoryMiB = int
GpuTotalMemoryMiB = int
GpuMemoryMiB = tuple[GpuUsedMemoryMiB, GpuTotalMemoryMiB]
GpuMemoryMiBList = list[GpuMemoryMiB]


# except if init doesn't set pynvml and then something tries to call get_metrics
class PynvmlNotAvailableError(Exception):
    pass


class GpuCollector(MetricCollector):
    def __init__(self):
        self.pynvml_active = False

        try:
            pynvml.nvmlInit()
            self.pynvml_active = True
        except pynvml.NVMLError_LibraryNotFound:
            # print("NVML Shared Library Not Found")  # This is the error I get locally. Do the others matter?
            pass
        except pynvml.NVMLError_DriverNotLoaded:
            print("NVIDIA Driver Not Loaded")
        except pynvml.NVMLError:
            print("Unexpected NVML error")
        except Exception as e:
            print(f"Unexpected error: {e}")

        if self.pynvml_active:
            self.device_count = pynvml.nvmlDeviceGetCount()
            self.handles = [
                pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.device_count)
            ]

    def collect(self) -> tuple[GpuUtilList, GpuMemoryMiBList]:
        if not self.pynvml_active:
            raise PynvmlNotAvailableError(
                "Failed to get metrics because pynvml was not found. After init, "
                "you must check pynvml_active before trying to call get_metrics"
            )
        gpu_util_list = [
            pynvml.nvmlDeviceGetUtilizationRates(handle).gpu for handle in self.handles
        ]
        gpu_memory_list = []

        for handle in self.handles:
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            # TODO: Confirm this is bytes
            memory_used_mib = memory.used / 1024 / 1024
            memory_total_mib = memory.total / 1024 / 1024
            memory_datapoint = (memory_used_mib, memory_total_mib)
            gpu_memory_list.append(memory_datapoint)

        return gpu_util_list, gpu_memory_list

    def collect_and_render(self, live: Live):
        if self.pynvml_active:
            gpu_util_list, gpu_memory_list = self.collect()
            # TODO: Fix this render
            gpu_util_str = ", ".join([f"{util}%" for util in gpu_util_list])
            gpu_memory_str = ", ".join(
                [f"{used:.2f}/{total:.2f} MiB" for used, total in gpu_memory_list]
            )
            live.update(
                f"GPU Utilization: {gpu_util_str}\nGPU Memory: {gpu_memory_str}"
            )
        else:
            live.update("[red bold]GPU metrics not available")

    def shutdown(self):
        if self.pynvml_active:
            pynvml.nvmlShutdown()
