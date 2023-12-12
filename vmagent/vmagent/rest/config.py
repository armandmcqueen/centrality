import os
import json
from pydantic import BaseModel

from common.constants import VM_AGENT_REST_CONFIG_ENVVAR


class VmAgentRestConfigEnvvarNotSetError(Exception):
    pass


# TODO: Abstract the RestConfig logic? The ControlPlaneRestConfig is basically identical
class VmAgentRestConfig(BaseModel):
    port: int
    startup_healthcheck_timeout: int
    startup_healthcheck_poll_interval: float = 0.5

    def save_to_envvar(self):
        os.environ[VM_AGENT_REST_CONFIG_ENVVAR] = self.model_dump_json()

    @classmethod
    def from_envvar(cls):
        config_json_str = os.environ.get(VM_AGENT_REST_CONFIG_ENVVAR, None)
        if config_json_str is None:
            raise VM_AGENT_REST_CONFIG_ENVVAR()
        config_json = json.loads(config_json_str)
        return cls(**config_json)


class DefaultVmAgentRestConfig(VmAgentRestConfig):
    def __init__(self):
        super().__init__(
            port=7777,
            startup_healthcheck_timeout=20,
        )
