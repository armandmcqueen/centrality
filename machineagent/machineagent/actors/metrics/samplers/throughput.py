import time


class Throughput:
    """Calculate the throughput of a value over time."""

    def __init__(self, start_val: float):
        self.begin_time = time.time()
        self.begin_val = start_val

    def add(self, new_val: float) -> float:
        """
        Add a new value and return the throughput since the last addition.
        """
        now = time.time()
        delta_val = new_val - self.begin_val
        delta_time = now - self.begin_time
        throughput = delta_val / delta_time

        self.begin_val = new_val
        self.begin_time = now

        return throughput
