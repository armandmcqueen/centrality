#####################################################################
# Endpoints                                                         #
#####################################################################

# Shared endpoints
HEALTHCHECK_ENDPOINT = "/healthz"
AUTH_HEALTHCHECK_ENDPOINT = "/healthz/auth"

# Control Plane specific endpoints
CONTROL_PLANE_CPU_METRIC_ENDPOINT = "/metrics/cpu"
CONTROL_PLANE_LATEST_CPU_METRIC_ENDPOINT = "/metrics/cpu/latest"
CONTROL_PLANE_VM_LIST_ENDPOINT = "/vm/list"
CONTROL_PLANE_VM_HEARTBEAT_ENDPOINT = "/vm/heartbeat/{vm_id}"


def get_control_plane_vm_heartbeat_endpoint(vm_id: str) -> str:
    return f"/vm/heartbeat/{vm_id}"


#####################################################################
# Actors                                                            #
#####################################################################

# VM Agent actors
VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR = "cpu_metric_collector"
VM_AGENT_HEARTBEAT_SENDER_ACTOR = "heartbeat_sender"


#####################################################################
# Other Constants                                                   #
#####################################################################
VM_HEARTBEAT_INTERVAL_SECS = 5  # How often VMs should report heartbeats
VM_HEARTBEAT_TIMEOUT_SECS = 10  # If not heartbeat for this long, consider it dead


# Control Plane specific constants
CONTROL_PLANE_REST_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_REST_CONFIG"
CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_DATASTORE_CONFIG"


# VM Agent specific constants
VM_AGENT_REST_CONFIG_ENVVAR = "CENTRALITY_VM_AGENT_REST_CONFIG"
VM_AGENT_METRIC_CPU_INTERVAL_SECS = 0.5  # How often to collect CPU metrics
