import pynvml
from rich import print
from rich.live import Live
from rich.table import Table
from vmagent.actors.metrics.samplers.sampler import MetricSampler


GpuUtil = float
GpuUtilList = list[GpuUtil]
GpuUsedMemoryMiB = int
GpuTotalMemoryMiB = int
GpuMemoryUsedMiBTotalMiB = tuple[GpuUsedMemoryMiB, GpuTotalMemoryMiB]
GpuMemoryUsedMiBTotalMibList = list[GpuMemoryUsedMiBTotalMiB]


# except if init doesn't set pynvml and then something tries to call get_metrics
class PynvmlNotAvailableError(Exception):
    pass


class GpuSampler(MetricSampler):
    def __init__(self):
        self.pynvml_available = False

        try:
            pynvml.nvmlInit()
            self.pynvml_available = True
        except pynvml.NVMLError_LibraryNotFound:
            # print("NVML Shared Library Not Found")  # This is the error I get locally. Do the others matter?
            pass
        except pynvml.NVMLError_DriverNotLoaded:
            print("NVIDIA Driver Not Loaded")
        except pynvml.NVMLError:
            print("Unexpected NVML error")
        except Exception as e:
            print(f"Unexpected error: {e}")

        if self.pynvml_available:
            self.device_count = pynvml.nvmlDeviceGetCount()
            self.handles = [
                pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.device_count)
            ]

    def sample(self) -> tuple[GpuUtilList, GpuMemoryUsedMiBTotalMibList]:
        if not self.pynvml_available:
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
            memory_used_mib = memory.used / 1024 / 1024
            memory_total_mib = memory.total / 1024 / 1024
            memory_datapoint = (memory_used_mib, memory_total_mib)
            gpu_memory_list.append(memory_datapoint)

        return gpu_util_list, gpu_memory_list

    def sample_and_render(self, live: Live):
        if self.pynvml_available:
            table = Table()
            gpu_util_list, gpu_memory_list = self.sample()
            header = [
                "GPU",
                "Utilization %",
                "Memory Used MiB",
                "Memory Total MiB",
                "Memory Used %",
            ]
            table.add_column(header[0])
            table.add_column(header[1])
            table.add_column(header[2])
            table.add_column(header[3])
            table.add_column(header[4])
            for i in range(self.device_count):
                gpu_util = gpu_util_list[i]
                memory_used_mib, memory_total_mib = gpu_memory_list[i]
                memory_used_percent = round(memory_used_mib / memory_total_mib * 100, 2)
                table.add_row(
                    str(i),
                    str(gpu_util),
                    str(memory_used_mib),
                    str(memory_total_mib),
                    str(memory_used_percent) + "%",
                )
            live.update(table)

        else:
            live.update("[red bold]GPU metrics not available")

    def shutdown(self):
        if self.pynvml_available:
            pynvml.nvmlShutdown()
