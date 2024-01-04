from centrality_controlplane_sdk import DataApi, CpuMeasurement
import datetime
from rich import print
from ..utils.utils import print_test_function_name
from . import constants as test_constants
from vmagent.machineinfo.config import MachineInfoConfig
from vmagent.machineinfo.machineinfo import get_machine_info


VM_ID = "vm-sdk"


def test_sdk_basics(docker_compose, sdk):
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
    live_vms = sdk.list_live_vms()
    assert (
        len(live_vms) == test_constants.EXPECTED_NUM_AGENTS
    ), f"Expected there to be {test_constants.EXPECTED_NUM_AGENTS} live VMs, got {len(live_vms)} VMs ({live_vms})"

    # Add one via heartbeat and confirm there are now 5
    machine_info_config = MachineInfoConfig(use_fake=True)
    sdk.register_vm(
        vm_id=VM_ID, vm_registration_info=get_machine_info(machine_info_config)
    )
    # sdk.report_vm_heartbeat(vm_id=VM_ID)
    live_vms = sdk.list_live_vms()
    new_expected_num_agents = test_constants.EXPECTED_NUM_AGENTS + 1
    assert (
        len(live_vms) == new_expected_num_agents
    ), f"Expected there to be {new_expected_num_agents} live VMs, got {len(live_vms)} VMs ({live_vms})"

    # Remove one via death and confirm we go back to test_constants.EXPECTED_NUM_AGENTS
    sdk.report_vm_death(vm_id=VM_ID)
    live_vms = sdk.list_live_vms()
    assert (
        len(live_vms) == test_constants.EXPECTED_NUM_AGENTS
    ), f"Expected there to be {test_constants.EXPECTED_NUM_AGENTS} live VMs, got {len(live_vms)} VMs ({live_vms})"


def test_cpu_measurements(docker_compose, sdk: DataApi):
    print_test_function_name()

    measurement = CpuMeasurement(
        vm_id=VM_ID,
        ts=datetime.datetime.now(datetime.timezone.utc),
        cpu_percents=[1, 2, 3],
    )
    sdk.put_cpu_metric(measurement)
    latest_ts = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=5
    )
    latest_cpu_percents = [10, 20, 30]
    measurement2 = CpuMeasurement(
        vm_id=VM_ID,
        ts=latest_ts,
        cpu_percents=latest_cpu_percents,
    )
    sdk.put_cpu_metric(measurement2)

    metrics = sdk.get_cpu_metrics(vm_ids=[VM_ID])
    assert len(metrics) == 2, f"Expected 2 metrics, got {len(metrics)}"

    latest_metrics = sdk.get_latest_cpu_metrics(vm_ids=[VM_ID])
    assert (
        len(latest_metrics) == 1
    ), f"Expected 1 latest metrics, got {len(latest_metrics)}"
    latest_metric = latest_metrics[0]
    assert (
        latest_metric.ts == latest_ts
    ), f"Latest metric ts ({latest_metric.ts}) doesn't match expected ({latest_ts})"
    assert latest_metric.cpu_percents == latest_cpu_percents, (
        f"Latest metric cpu_percents ({latest_metric.cpu_percents}) doesn't "
        f"match expected ({latest_cpu_percents})"
    )
