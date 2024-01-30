import pytest
import subprocess
from pathlib import Path
from centrality_controlplane_sdk import DataApi
from common.sdks.controlplane.sdk import ControlPlaneSdkConfig
from common.utils.wait_for_healthy import wait_for_healthy
from common import constants
from common.sdks.controlplane.sdk import get_sdk
from rich import print
import datetime
import time





def main():
    sdk_config = ControlPlaneSdkConfig()
    client = get_sdk(sdk_config, token=constants.CONTROL_PLANE_SDK_DEV_TOKEN)
    resp = client.get_healthcheck()
    machines = client.get_live_machines()
    print(machines)
    machine_ids = [m.machine_id for m in machines]
    print(machine_ids)

    now = datetime.datetime.utcnow()
    query_start = now - datetime.timedelta(minutes=1)

    machine_id = "fake-data"
    print()
    print()
    print("**********")
    #
    # print("Running get_latest_cpu_metrics")
    # r = client.get_latest_cpu_metrics(machine_ids=[machine_id])
    # print(r)
    # print("Finished get_latest_cpu_metrics")
    # print("--------------------")
    #
    # print("Running get_latest_memory_metrics")
    # r = client.get_latest_memory_metrics(machine_ids=[machine_id])
    # print(r)
    # print("Finished get_latest_memory_metrics")
    # print("--------------------")

    print("Running get_latest_disk_throughput_metrics")
    r = client.get_latest_disk_throughput_metrics(machine_ids=[machine_id])
    print(r)
    print("Finished get_latest_disk_throughput_metrics")
    print("--------------------")

    print("Running get_disk_throughput_metrics")
    r = client.get_disk_throughput_metrics(machine_ids=[machine_id], from_ts=query_start, to_ts=now)
    print(r)
    print("Finished get_disk_throughput_metrics")
    print("--------------------")


    #
    # print("Running get_latest_nvidia_smi_metrics")
    # r = client.get_latest_nvidia_smi_metrics(machine_ids=[machine_id])
    # print(r)
    # print("Finished get_latest_nvidia_smi_metrics")
    # print("--------------------")
    #
    # print("Running get_latest_disk_usage_metrics")
    # r = client.get_latest_disk_usage_metrics(machine_ids=[machine_id])
    # print(r)
    # print("Finished get_latest_disk_usage_metrics")
    # print("--------------------")
    #
    # print("Running get_latest_network_throughput_metrics")
    # r = client.get_latest_network_throughput_metrics(machine_ids=[machine_id])
    # print(r)
    # print("Finished get_latest_network_throughput_metrics")
    # print("--------------------")
    #
    # r = client.get_latest_disk_iops_metrics(machine_ids=[machine_id])
    # print(r)
    #
    # r = client.get_latest_gpu_utilization_metrics(machine_ids=[machine_id])
    # print(r)
    #
    # r = client.get_latest_gpu_memory_metrics(machine_ids=[machine_id])
    # print(r)




if __name__ == '__main__':
    main()