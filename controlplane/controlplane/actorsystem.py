from controlplane.datastore.config import DatastoreConfig
import conclib
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
        # Check if the message is a RequestEnvelope (i.e. a message that arrived from
        # outside the actor system)
        if isinstance(message, conclib.RequestEnvelope):
            pass  # TODO: Implement messages from outside the actor system
            # req_envelope = message
            # # Check which type of message was received and extract it. We cannot do an
            # # isinstance() check due to how the RequestEnvelope is implemented.
            # if req_envelope.matches(ExampleRequestMessage):
            #     actor_message = req_envelope.extract(ExampleRequestMessage)
            #     type(actor_message)  # ExampleRequestMessage
            #
            #     # DO SOMETHING WITH THE MESSAGE
            #
            #     # Send a response back to the sender
            #     req_envelope.respond(ExampleResponseMessage())
            # else:
            #     raise conclib.errors.UnexpectedMessageError(message)
        else:
            if isinstance(message, PreviewerTick):
                pass
            else:
                raise conclib.errors.UnexpectedMessageError(message)
