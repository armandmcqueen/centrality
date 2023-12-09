import os
import json
from dataclasses import dataclass
from pydantic import BaseModel
from controlplane.constants import CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR


class ControlPlaneDatastoreConfigEnvvarNotSetError(Exception):
    pass


class DatastoreConfig(BaseModel):
    host: str
    port: str
    username: str
    password: str
    verbose_orm: bool

    def get_url(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}"

    def save_to_envvar(self):
        os.environ[CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR] = self.model_dump_json()

    @classmethod
    def from_envvar(cls):
        config_json_str = os.environ.get(CONTROL_PLANE_DATASTORE_CONFIG_ENVVAR, None)
        if config_json_str is None:
            raise ControlPlaneDatastoreConfigEnvvarNotSetError()
        config_json = json.loads(config_json_str)
        return cls(**config_json)


class DefaultDatastoreConfig(DatastoreConfig):
    def __init__(self):
        super().__init__(
            host="localhost",
            port="5432",
            username="postgres",
            password="postgres",
            verbose_orm=False,
        )
