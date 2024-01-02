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

    def __init__(
        self,
        datastore_config: DatastoreConfig,
        datastore_sweeper_config: DatastoreSweeperConfig,
    ):
        self.datastore_config = datastore_config
        self.datastore_sweeper_config = datastore_sweeper_config
        self.datastore_tasks_subsystem = DatastoreTasksSubsystem(
            datastore_config=self.datastore_config,
            datastore_sweeper_config=self.datastore_sweeper_config,
        )

    def start(self) -> "ControlPlaneActorSystem":
        self.datastore_tasks_subsystem.start()
        return self


class DatastoreTasksSubsystem:
    """
    Container for datastore tasks.
    """

    def __init__(
        self,
        datastore_config: DatastoreConfig,
        datastore_sweeper_config: DatastoreSweeperConfig,
    ):
        self.datastore_config = datastore_config
        self.datastore_sweeper_config = datastore_sweeper_config
        self.datastore_sweeper_ref: Optional[pykka.ActorRef[DatastoreSweeper]] = None

    def start(self) -> None:
        self.datastore_config = DatastoreSweeper.start(
            datastore_sweeper_config=self.datastore_sweeper_config,
            datastore_config=self.datastore_config,
        )
