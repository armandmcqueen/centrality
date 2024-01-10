from centrality_controlplane_sdk import DataApi, CpuMeasurement
from datetime import datetime, timezone, timedelta
from rich import print
from ..utils.utils import print_test_function_name
from ..utils import asserts
from . import constants as test_constants
from vmagent.machineinfo.config import MachineInfoConfig
from vmagent.machineinfo.machineinfo import get_machine_info


VM_ID = "vm-sdk"


def test_sdk_basics(docker_compose, sdk):
    """Run basic SDK functions and make sure they don't error"""
    print_test_function_name()

    health_resp = sdk.get_healthcheck()
    print(f"Healthcheck response: {health_resp}")
    health_auth_resp = sdk.get_auth_healthcheck()
    print(f"Authed healthcheck response: {health_auth_resp}")
    info_resp = sdk.get_info()
    print(f"Info response: {info_resp}")


def test_vm_liveness(docker_compose, sdk: DataApi):
    """Test listing vms, adding live vms via heartbeats, and removing VMs via reporting death"""
    print_test_function_name()

    # Confirm that we start with test_constants.EXPECTED_NUM_AGENTS
    asserts.list_size(sdk.list_live_vms(), test_constants.EXPECTED_NUM_AGENTS)

    # Register a new VM and confirm there are now test_constants.EXPECTED_NUM_AGENTS + 1
    machine_info_config = MachineInfoConfig(use_fake=True)
    sdk.register_vm(
        vm_id=VM_ID, vm_registration_info=get_machine_info(machine_info_config)
    )
    asserts.list_size(sdk.list_live_vms(), test_constants.EXPECTED_NUM_AGENTS + 1)

    # Remove one via death and confirm we go back to test_constants.EXPECTED_NUM_AGENTS
    sdk.report_vm_death(vm_id=VM_ID)
    asserts.list_size(sdk.list_live_vms(), test_constants.EXPECTED_NUM_AGENTS)


# TODO: Test other metrics via parametrization
def test_cpu_measurements(docker_compose, sdk: DataApi):
    print_test_function_name()

    # Write two CPU measurements and confirm we can read them back
    measurement = CpuMeasurement(
        vm_id=VM_ID,
        ts=datetime.now(timezone.utc),
        cpu_percents=[1, 2, 3],
    )
    latest_ts = datetime.now(timezone.utc) + timedelta(seconds=5)
    latest_cpu_percents = [10, 20, 30]
    measurement2 = CpuMeasurement(
        vm_id=VM_ID,
        ts=latest_ts,
        cpu_percents=latest_cpu_percents,
    )
    sdk.put_cpu_metric(measurement)
    sdk.put_cpu_metric(measurement2)

    # Confirm that there are the two we expect
    asserts.list_size(sdk.get_cpu_metrics(vm_ids=[VM_ID]), 2)

    # Confirm that the correct one is the latest one
    latest_metrics = sdk.get_latest_cpu_metrics(vm_ids=[VM_ID])
    asserts.list_size(latest_metrics, 1)
    asserts.matches(latest_metrics[0].ts, latest_ts)
    asserts.matches(latest_metrics[0].cpu_percents, latest_cpu_percents)
