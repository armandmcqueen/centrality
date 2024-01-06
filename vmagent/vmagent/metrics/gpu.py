import pynvml
from rich import print

GpuUtil = float
GpuUtilList = list[GpuUtil]
GpuUsedMemory = int
GpuTotalMemory = int
GpuMemory = tuple[GpuUsedMemory, GpuTotalMemory]
GpuMemoryList = list[GpuMemory]


# except if init doesn't set pynvml and then something tries to call get_metrics
class PynvmlNotAvailableError(Exception):
    pass


class GpuMonitor:
    def __init__(self):
        self.pynvml_active = False
        try:
            pynvml.nvmlInit()
            self.pynvml_found = True
        except pynvml.NVMLError_LibraryNotFound:
            print("NVML Shared Library Not Found")
        except pynvml.NVMLError_DriverNotLoaded:
            print("NVIDIA Driver Not Loaded")
        except pynvml.NVMLError:
            print("Unexpected NVML error")
        except Exception as e:
            print(f"Unexpected error: {e}")

        if self.pynvml_found:
            self.device_count = pynvml.nvmlDeviceGetCount()
            self.handles = [
                pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.device_count)
            ]

    def get_metrics(self) -> tuple[GpuUtilList, GpuMemoryList]:
        if not self.pynvml_found:
            raise PynvmlNotAvailableError(
                "Failed to get metrics because pynvml was not found. After init, "
                "you must check pynvml_active before trying to call get_metrics"
            )
        gpu_util_list = []
        gpu_memory_list = []

        for handle in self.handles:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

            gpu_util_list.append(util.gpu)
            gpu_memory_list.append((memory.used, memory.total))

        return gpu_util_list, gpu_memory_list

    # Pycharm is complaining that this can be a static method, but it's wrong. How do I tell it that?
    def shutdown(self):
        pynvml.nvmlShutdown()


def main():
    GpuMonitor()


"""
import pynvml

# Initialize NVML
pynvml.nvmlInit()

# Function to retrieve GPU utilization, GPU memory usage, and processes
def get_gpu_info():
    

# Retrieve GPU information
gpu_info = get_gpu_info()

# Cleanup
pynvml.nvmlShutdown()

"""


if __name__ == "__main__":
    main()
