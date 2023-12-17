from typing import Callable
import sys


def _no_op():
    pass


class CliContextManager:
    """ Context manager that handles keyboard interrupts, exceptions and goodbye messages """
    def __init__(self, finally_func: Callable = _no_op):
        self.finally_func = finally_func

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is KeyboardInterrupt:
            print()
            print("🛑 Received keyboard interrupt.")
        elif exc_type is not None:
            print("❗️ Encountered an error")
            print(exc_value)
        self.finally_func()
        print("👋 Goodbye")
        sys.exit(0)  # Prevent any other output from happening
