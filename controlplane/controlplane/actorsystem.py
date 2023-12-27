from controlplane.datastore.config import DatastoreConfig
import pykka
from typing import Optional


class ControlPlaneActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """

    def __init__(
        self,
        datastore_config: DatastoreConfig,
    ):
        self.datastore_config = datastore_config
        self.example_subsystem = ExampleSubsystem(self.datastore_config)

    def start(self) -> "ControlPlaneActorSystem":
        self.example_subsystem.start()
        return self


class ExampleSubsystem:
    """
    Container for an example subsystem
    """

    def __init__(
        self,
        datastore_config: DatastoreConfig,
    ):
        self.datastore_config = datastore_config
        self.example_actor_ref: Optional[pykka.ActorRef] = None

    def start(self):
        # self.example_actor_ref = ExampleActor.start(
        #     datastore_config=self.datastore_config,
        # )
        pass
