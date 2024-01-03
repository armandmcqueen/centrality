import controlplane_sdk
import datetime
from rich import print


def test_sdk_v2_basics(docker_compose, sdk_v2):
    health_resp = sdk_v2.get_healthcheck()
    print(f"Healthcheck response: {health_resp}")
    health_auth_resp = sdk_v2.get_auth_healthcheck()
    print(f"Authed healthcheck response: {health_auth_resp}")
    info_resp = sdk_v2.get_info()
    print(f"Info response: {info_resp}")


def test_sdk_v2_operations(docker_compose, sdk_v2):
    VM_ID = "vm-sdk2"

    vms = sdk_v2.list_live_vms()
    assert len(vms) == 4, f"Expected there to be 4 live VMs, got {len(vms)} VMs ({vms})"
    sdk_v2.report_heartbeat(vm_id=VM_ID)
    new_vms = sdk_v2.list_live_vms()
    assert (
        len(new_vms) == 5
    ), f"Expected there to be 5 live VMs, got {len(new_vms)} VMs ({new_vms})"

    measurement = controlplane_sdk.CpuMeasurement(
        vm_id=VM_ID,
        ts=datetime.datetime.now(datetime.timezone.utc),
        cpu_percents=[1, 2, 3],
    )
    sdk_v2.put_cpu_metric(measurement)
    latest_ts = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=5
    )
    latest_cpu_percents = [10, 20, 30]
    measurement2 = controlplane_sdk.CpuMeasurement(
        vm_id=VM_ID,
        ts=latest_ts,
        cpu_percents=latest_cpu_percents,
    )
    sdk_v2.put_cpu_metric(measurement2)

    metrics = sdk_v2.get_cpu_metrics(vm_ids=[VM_ID])
    assert len(metrics) == 2, f"Expected 2 metrics, got {len(metrics)}"

    latest_metrics = sdk_v2.get_latest_cpu_metrics(vm_ids=[VM_ID])
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
