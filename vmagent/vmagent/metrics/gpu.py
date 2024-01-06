import pynvml
from rich import print
from rich.console import Console
from rich.live import Live

GpuUtil = float
GpuUtilList = list[GpuUtil]
GpuUsedMemoryMiB = int
GpuTotalMemoryMiB = int
GpuMemoryMiB = tuple[GpuUsedMemoryMiB, GpuTotalMemoryMiB]
GpuMemoryMiBList = list[GpuMemoryMiB]


# except if init doesn't set pynvml and then something tries to call get_metrics
class PynvmlNotAvailableError(Exception):
    pass


class GpuMonitor:
    def __init__(self, fake=False, fake_gpu_count=1):
        self.fake = fake
        self.fake_gpu_count = fake_gpu_count

        self.pynvml_active = False

        try:
            pynvml.nvmlInit()
            self.pynvml_active = True
        except pynvml.NVMLError_LibraryNotFound:
            print("NVML Shared Library Not Found")
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

    def get_real_metrics(self) -> tuple[GpuUtilList, GpuMemoryMiBList]:
        if not self.pynvml_active:
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
            gpu_memory_list.append(
                (memory.used / 1024 / 1024, memory.total / 1024 / 1024)
            )

        return gpu_util_list, gpu_memory_list

    # Pycharm is complaining that this can be a static method, but it's wrong. How do I tell it that?
    def shutdown(self):
        pynvml.nvmlShutdown()


def main():
    import pytest

    mon = GpuMonitor()
    console = Console()
    try:
        with Live(console=console, refresh_per_second=10, transient=True) as live:
            if mon.pynvml_active:
                while True:
                    util, mem = mon.get_real_metrics()

                    used = [m[0] for m in mem]
                    totals = [m[1] for m in mem]

                    # Create formatted output
                    output = f"util %: {util}\nused MiB: {used}\ntotal MiB: {totals}"

                    # Update the Live display
                    live.update(output)

            else:
                with pytest.raises(PynvmlNotAvailableError):
                    mon.get_real_metrics()
    except KeyboardInterrupt:
        print("[red]Aborted")
    finally:
        mon.shutdown()


if __name__ == "__main__":
    main()
