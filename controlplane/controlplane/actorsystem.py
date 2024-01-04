import pykka
from typing import Optional
from controlplane.datastore.config import DatastoreConfig
from controlplane.actors.datastore_sweeper import (
    DatastoreSweeper,
    DatastoreSweeperConfig,
)


class ControlPlaneActorSystem:
    """
    Root container for the actor system. Just a container for keeping things organized.

    Technically there is a conclib actor that is part of the pykka actor system, but isn't here
    """

    # TODO: Implement machine registration reaping

    def __init__(
        self,
        datastore_config: DatastoreConfig,
        datastore_sweeper_config: DatastoreSweeperConfig,
    ):
        self.datastore_config = datastore_config
        self.datastore_sweeper_config = datastore_sweeper_config
        self.datastore_sweeper_ref: Optional[pykka.ActorRef[DatastoreSweeper]] = None

    def start(self) -> "ControlPlaneActorSystem":
        self.datastore_sweeper_ref = DatastoreSweeper.start(
            datastore_sweeper_config=self.datastore_sweeper_config,
            datastore_config=self.datastore_config,
        )
        return self
