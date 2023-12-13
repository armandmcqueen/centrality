#####################################################################
# Endpoints                                                         #
#####################################################################

# Shared endpoints
HEALTHCHECK_ENDPOINT = "/healthz"
AUTH_HEALTHCHECK_ENDPOINT = "/healthz/auth"

# Control Plane specific endpoints
CONTROL_PLANE_CPU_METRIC_ENDPOINT = "/metrics/cpu"


#####################################################################
# Actors                                                            #
#####################################################################

# VM Agent actors
VM_AGENT_CPU_METRIC_COLLECTOR_ACTOR = "cpu_metric_collector"


#####################################################################
# Other Constants                                                   #
#####################################################################
# Control Plane specific constants
CONTROL_PLANE_REST_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_REST_CONFIG"
CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR = "CENTRALITY_CONTROL_PLANE_DATASTORE_CONFIG"

# VM Agent specific constants
VM_AGENT_REST_CONFIG_ENVVAR = "CENTRALITY_VM_AGENT_REST_CONFIG"


