# Template for writing the boilerplate of an actor with a ticker

import conclib
import pykka

from types import TracebackType
from typing import Optional

from common import constants


class TickMessage(conclib.ActorMessage):
    pass


class ExampleActor(conclib.Actor):
    URN = constants.YOUR_ACTOR_URN  # TODO: Replace with your actor's URN

    def __init__(self):
        self.ticker: Optional[ExampleTicker] = None
        super().__init__(
            urn=self.URN,
        )

    def on_start(self) -> None:
        self.ticker = ExampleTicker(self.actor_ref)
        self.ticker.start()

    def on_stop(self) -> None:
        self.ticker.stop()

    def on_failure(
        self,
        exception_type: Optional[type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.ticker.stop()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, TickMessage):
            # TODO: DO SOMETHING
            pass
        else:
            raise conclib.errors.UnexpectedMessageError(message)


class ExampleTicker(conclib.Ticker):
    TICK_INTERVAL = 0.5  # TODO: Change this to the desired interval

    def __init__(self, example_actor_ref: pykka.ActorRef):
        self.example_actor_ref = example_actor_ref
        super().__init__(interval=self.TICK_INTERVAL)

    def execute(self):
        self.example_actor_ref.tell(TickMessage())
