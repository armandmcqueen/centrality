from controlplane.datastore.config import DatastoreConfig
from controlplane.actors.previewer import Previewer
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
        self.previewer_subsystem = PreviewerSubsystem(self.datastore_config)

    def start(self) -> "ControlPlaneActorSystem":
        self.previewer_subsystem.start()
        return self


class PreviewerSubsystem:
    """
    Container for the Previewer subsystem
    """
    def __init__(
            self,
            datastore_config: DatastoreConfig,
    ):
        self.datastore_config = datastore_config
        self.previewer_actor_ref: Optional[pykka.ActorRef] = None

    def start(self):
        self.previewer_actor_ref = Previewer.start(
            datastore_config=self.datastore_config,
        )


