from typing import Callable, Optional
from types import TracebackType


def _no_op() -> None:
    pass


FinallyFunc = Callable[[], None]


class CliContextManager:
    """Context manager that handles keyboard interrupts, exceptions and goodbye messages"""

    def __init__(self, finally_func: FinallyFunc = _no_op):
        self.finally_func = finally_func

    def __enter__(self) -> "CliContextManager":
        return self

    def __exit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]) -> bool:
        suppress_exception = False
        if exc_type is KeyboardInterrupt:
            print()
            print("🛑 Received keyboard interrupt.")
            suppress_exception = True
        elif exc_type is not None:
            print("❗️ Encountered an error")
            print(exc_value)
        self.finally_func()
        print("👋 Goodbye")
        return suppress_exception
