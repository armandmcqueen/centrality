import os
import json
from pydantic import BaseModel

from controlplane.constants import CONTROL_PLANE_REST_CONFIG_ENVVAR


class ControlPlaneRestConfigEnvvarNotSetError(Exception):
    pass


class ControlPlaneRestConfig(BaseModel):
    port: int
    startup_healthcheck_timeout: float
    startup_healthcheck_poll_interval: float = 0.5

    def save_to_envvar(self):
        os.environ[CONTROL_PLANE_REST_CONFIG_ENVVAR] = self.model_dump_json()

    @classmethod
    def from_envvar(cls):
        config_json_str = os.environ.get(CONTROL_PLANE_REST_CONFIG_ENVVAR, None)
        if config_json_str is None:
            raise ControlPlaneRestConfigEnvvarNotSetError()
        config_json = json.loads(config_json_str)
        return cls(**config_json)


class DefaultControlPlaneRestConfig(ControlPlaneRestConfig):
    def __init__(self):
        super().__init__(
            port=8000,
            startup_healthcheck_timeout=20,
        )


