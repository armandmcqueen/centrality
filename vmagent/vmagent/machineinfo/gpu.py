from typing import Optional
import subprocess

NumGpus = int
GpuType = Optional[str]
GpuMemoryMiB = Optional[int]
NvidiaDriverVersion = Optional[str]


def get_nvidia_gpu_info() -> tuple[NumGpus, GpuType, GpuMemoryMiB, NvidiaDriverVersion]:
    try:
        # Run the nvidia-smi command to get GPU details
        gpu_details = (
            subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=gpu_name,memory.total,driver_version",
                    "--format=csv,noheader",
                ]
            )
            .decode("utf-8")
            .strip()
        )

        # Split the output into lines, each representing a GPU
        gpu_lines = gpu_details.split("\n")

        # Extract GPU type and memory
        gpu_info = []
        for line in gpu_lines:
            if line:
                gpu_name, gpu_memory, diver_version = [
                    s.strip() for s in line.split(", ")
                ]
                memory_mb, unit = gpu_memory.split()
                if unit != "MiB":
                    raise Exception(f"[MachineInfo.gpu] Unexpected unit: {unit}")
                memory_mb = int(memory_mb.strip())
                gpu_info.append(
                    {
                        "name": gpu_name.strip(),
                        "memory_mb": memory_mb,
                        "driver_version": diver_version,
                    }
                )

        # confirm all gpus are identical in all ways
        for gpu in gpu_info:
            assert gpu == gpu_info[0]

        return (
            len(gpu_info),
            gpu_info[0]["name"],
            gpu_info[0]["memory_mb"],
            gpu_info[0]["driver_version"],
        )

    except subprocess.CalledProcessError as e:
        # Handle errors if nvidia-smi is not found or another error occurs
        print("[MachineInfo.gpu] An error occurred:", e)
        return 0, None, None, None
    except FileNotFoundError:
        # nvidia-smi doesn't exist. This is expected in many cases
        return 0, None, None, None
    except Exception as e:
        # Handle any other exceptions
        print("[MachineInfo.gpu] An error occurred:", e)
        return 0, None, None, None


if __name__ == "__main__":
    # Get the NVIDIA GPU details
    num_gpus, gpu_type, gpu_memory_mb, nvidia_driver_version = get_nvidia_gpu_info()
    print(f"num_gpus: {num_gpus}")
    print(f"gpu_type: {gpu_type}")
    print(f"gpu_memory_mib: {gpu_memory_mb}")
    print(f"nvidia_driver_version: {nvidia_driver_version}")
