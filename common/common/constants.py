#####################################################################
# Endpoints                                                         #
#####################################################################

# Shared endpoints
HEALTHCHECK_ENDPOINT = "/healthz"
AUTH_HEALTHCHECK_ENDPOINT = "/healthz/auth"
INFO_ENDPOINT = "/info"

# Control Plane specific endpoints
CONTROL_PLANE_CPU_METRIC_ENDPOINT = "/metrics/cpu"
CONTROL_PLANE_LATEST_CPU_METRIC_ENDPOINT = "/metrics/cpu/latest"
CONTROL_PLANE_LIVE_VM_ENDPOINT = "/vm/live"
CONTROL_PLANE_VM_REGISTRATION_ENDPOINT = "/vm/{vm_id}/register"
CONTROL_PLANE_VM_HEARTBEAT_ENDPOINT = "/vm/{vm_id}/heartbeat"
CONTROL_PLANE_VM_DEATH_ENDPOINT = "/vm/{vm_id}/death"


def get_control_plane_vm_heartbeat_endpoint(vm_id: str) -> str:
    return f"/vm/heartbeat/{vm_id}"


#####################################################################
# Actors                                                            #
#####################################################################

# Control Plane actors
CONTROL_PLANE_DATASTORE_SWEEPER_ACTOR = "datastore_sweeper"

# VM Agent actors
VM_AGENT_HEARTBEAT_SENDER_ACTOR = "heartbeat_sender"

VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR = "cpu_metric_collector"
VM_AGENT_DISK_IO_METRIC_COLLECTOR_ACTOR = "disk_io_metric_collector"
VM_AGENT_DISK_MB_METRIC_COLLECTOR_ACTOR = "disk_mb_metric_collector"
VM_AGENT_GPU_METRIC_COLLECTOR_ACTOR = "gpu_metric_collector"
VM_AGENT_MEMORY_METRIC_COLLECTOR_ACTOR = "memory_metric_collector"
VM_AGENT_NETWORK_METRIC_COLLECTOR_ACTOR = "network_metric_collector"


#####################################################################
# Other Constants                                                   #
#####################################################################
VM_HEARTBEAT_INTERVAL_SECS = 5  # How often VMs should report heartbeats

# If no heartbeat for this long, consider it disconnected (limbo, not dead)
VM_NO_HEARTBEAT_LIMBO_SECS = 10

# If no heartbeat for this long, consider it dead. The final value is set through a
# config, this is just the default value
DEFAULT_VM_NO_HEARTBEAT_DEATH_SECS = 60 * 20


# Control Plane specific constants
CONTROL_PLANE_REST_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_REST_CONFIG"
CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_DATASTORE_CONFIG"
CONTROL_PLANE_SDK_DEV_TOKEN = "dev"


# VM Agent specific constants
VM_AGENT_REST_CONFIG_ENVVAR = "CENTRALITY_VM_AGENT_REST_CONFIG"
VM_AGENT_METRIC_CPU_INTERVAL_SECS = 0.1  # How often to collect CPU metrics
VM_AGENT_METRIC_DISK_INTERVAL_SECS = 0.1
VM_AGENT_METRIC_GPU_INTERVAL_SECS = 0.1
VM_AGENT_METRIC_MEMORY_INTERVAL_SECS = 0.1
VM_AGENT_METRIC_NETWORK_INTERVAL_SECS = 0.1
