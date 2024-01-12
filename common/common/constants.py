#####################################################################
# Endpoints                                                         #
#####################################################################

# Shared endpoints
HEALTHCHECK_ENDPOINT = "/healthz"
AUTH_HEALTHCHECK_ENDPOINT = "/healthz/auth"
INFO_ENDPOINT = "/info"

# TODO: Change this to have machine_id as URL param?
# Control Plane specific endpoints
CONTROL_PLANE_METRIC_CPU_ENDPOINT = "/machine/metrics/cpu"
CONTROL_PLANE_METRIC_DISK_IOPS_ENDPOINT = "/machine/metrics/disk-iops"
CONTROL_PLANE_METRIC_DISK_USAGE_ENDPOINT = "/machine/metrics/disk-usage"
CONTROL_PLANE_METRIC_DISK_THROUGHPUT_ENDPOINT = "/machine/metrics/disk-throughput"
CONTROL_PLANE_METRIC_GPU_MEMORY_ENDPOINT = "/machine/metrics/gpu-memory"
CONTROL_PLANE_METRIC_GPU_UTILIZATION_ENDPOINT = "/machine/metrics/gpu-utilization"
CONTROL_PLANE_METRIC_MEMORY_ENDPOINT = "/machine/metrics/memory"
CONTROL_PLANE_METRIC_NETWORK_THROUGHPUT_ENDPOINT = "/machine/metrics/network-throughput"
CONTROL_PLANE_METRIC_NVIDIA_SMI_ENDPOINT = "/machine/metrics/nvidia-smi"

CONTROL_PLANE_GET_LIVE_MACHINES_ENDPOINT = "/machine/live"
CONTROL_PLANE_GET_MACHINE_ENDPOINT = "/machine/{machine_id}"
CONTROL_PLANE_MACHINE_REGISTRATION_ENDPOINT = "/machine/{machine_id}/register"
CONTROL_PLANE_MACHINE_HEARTBEAT_ENDPOINT = "/machine/{machine_id}/heartbeat"
CONTROL_PLANE_MACHINE_DEATH_ENDPOINT = "/machine/{machine_id}/report-death"

# Disallowed machine names to preserve API endpoint structure
RESERVED_MACHINE_NAMES = ["live", "metrics"]


def get_control_plane_machine_heartbeat_endpoint(machine_id: str) -> str:
    return f"/machine/heartbeat/{machine_id}"


#####################################################################
# Actors                                                            #
#####################################################################

# Control Plane actors
CONTROL_PLANE_DATASTORE_SWEEPER_ACTOR = "datastore_sweeper"

# Machine Agent actors
MACHINE_AGENT_HEARTBEAT_SENDER_ACTOR = "heartbeat_sender"

MACHINE_AGENT_CPU_METRIC_COLLECTOR_ACTOR = "cpu_metric_collector"
MACHINE_AGENT_DISK_IO_METRIC_COLLECTOR_ACTOR = "disk_io_metric_collector"
MACHINE_AGENT_DISK_MB_METRIC_COLLECTOR_ACTOR = "disk_mb_metric_collector"
MACHINE_AGENT_GPU_METRIC_COLLECTOR_ACTOR = "gpu_metric_collector"
MACHINE_AGENT_MEMORY_METRIC_COLLECTOR_ACTOR = "memory_metric_collector"
MACHINE_AGENT_NETWORK_METRIC_COLLECTOR_ACTOR = "network_metric_collector"
MACHINE_AGENT_NVIDIA_SMI_METRIC_COLLECTOR_ACTOR = "nvidia_smi_collector"


#####################################################################
# Other Constants                                                   #
#####################################################################
MACHINE_HEARTBEAT_INTERVAL_SECS = 5  # How often machines should report heartbeats

# If no heartbeat for this long, consider it disconnected (limbo, not dead)
MACHINE_NO_HEARTBEAT_LIMBO_SECS = 10

# If no heartbeat for this long, consider it dead. The final value is set through a
# config, this is just the default value
DEFAULT_MACHINE_NO_HEARTBEAT_DEATH_SECS = 60 * 20


# Control Plane specific constants
CONTROL_PLANE_REST_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_REST_CONFIG"
CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_DATASTORE_CONFIG"
CONTROL_PLANE_SDK_DEV_TOKEN = "dev"


# Machine Agent specific constants
MACHINE_AGENT_REST_CONFIG_ENVVAR = "CENTRALITY_MACHINE_AGENT_REST_CONFIG"


# TODO: Make metric speed configurable
# Enable this to make metrics slower for testing other functionality
METRIC_SPEED = 0.25

MACHINE_AGENT_METRIC_CPU_INTERVAL_SECS = METRIC_SPEED
MACHINE_AGENT_METRIC_DISK_INTERVAL_SECS = METRIC_SPEED
MACHINE_AGENT_METRIC_GPU_INTERVAL_SECS = METRIC_SPEED
MACHINE_AGENT_METRIC_MEMORY_INTERVAL_SECS = METRIC_SPEED
MACHINE_AGENT_METRIC_NETWORK_INTERVAL_SECS = METRIC_SPEED
MACHINE_AGENT_METRIC_NVIDIA_SMI_INTERVAL_SECS = 5
