import conclib
from controlplane.datastore.config import DatastoreConfig


class PreviewerTick(conclib.ActorMessage):
    pass


class Previewer(conclib.PeriodicActor):
    URN = "previewer"  # TODO: Move to constants

    TICKS = {
        PreviewerTick: 1,  # Every 1 second
    }

    def __init__(self, datastore_config: DatastoreConfig):
        self.datastore_config = datastore_config
        super().__init__()

    def on_receive(self, message):
        if isinstance(message, PreviewerTick):
            pass
        else:
            raise conclib.errors.UnexpectedMessageError(message)