import subprocess
import psutil
import platform

UNKNOWN_CPU_DESCRIPTION = "Unknown CPU"


def sh(cmd) -> str:
    """Runs a shell command and returns the output as a string"""
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


def get_num_cpus() -> int:
    """Returns logical CPU count"""
    return psutil.cpu_count()


def get_linux_cpu_info() -> str:
    # This function retrieves CPU information on Linux, with some fallbacks to avoid meaningless output
    try:
        line = sh('lscpu | grep "Model name"')
        model_name = line.replace("Model name:", "").strip()
        if model_name != "":
            return model_name

    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            # This happens in graviton3 instances (and probably others we don't know about yet)
            # Don't log anything as this is expected
            pass
        else:
            print(
                f"[MachineInfo] Unexpected subprocess.CalledProcessError in lscpu + grep: {e}"
            )
            model_name = None
    except Exception as e:
        print(f"[MachineInfo] Unexpected Exception after lscpu: {e}")
        model_name = None

    # If we didn't get a good model_name, try dmidecode
    try:
        tmp = sh("sudo dmidecode -t processor | grep Version")
        model_name = tmp.replace("Version:", "").strip()
    except Exception as e:
        print(f"[MachineInfo] Unexpected Exception after dmidecode: {e}")
        model_name = ""

    if model_name in ["", "Not Specified"]:
        # TODO: Add other special cases as we encounter them
        print(
            "[MachineInfo] Unknown CPU - please report this at "
            "https://github.com/armandmcqueen/centrality/issues "
            "so we can add support for your case"
        )
        model_name = UNKNOWN_CPU_DESCRIPTION
    return model_name


def get_mac_cpu_info() -> str:
    # This function retrieves CPU information on macOS
    try:
        line = sh('sysctl -a | grep "brand_string"')
        model_name = line.replace("machdep.cpu.brand_string:", "").strip()
    except Exception as e:
        print(f"[MachineInfo] Unexpected Exception after sysctl + grep: {e}")
        model_name = UNKNOWN_CPU_DESCRIPTION
    return model_name


def get_cpu_description() -> str:
    """Returns CPU description, such as "Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz" """
    os_name = platform.system()

    if os_name == "Linux":
        try:
            cpu_info = get_linux_cpu_info()
        except Exception as e:
            print(f"[MachineInfo] {e}")
            cpu_info = "Failed to retrieve CPU info"
    elif os_name == "Darwin":
        try:
            cpu_info = get_mac_cpu_info()
        except Exception as e:
            print(f"[MachineInfo] {e}")
            cpu_info = "Failed to retrieve CPU info"
    else:
        raise NotImplementedError(f"Unsupported operating system: {os_name}")
    return cpu_info
