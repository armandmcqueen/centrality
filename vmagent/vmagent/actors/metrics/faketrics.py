from enum import Enum
from common.config.config import CentralityConfig
import time
import random


class FakeMetricAlgorithms(str, Enum):
    LINEAR_SYNCED = "linear_synced"
    RANDOM = "random"


class FakeMetricConfig(CentralityConfig):
    period: float = 20  # seconds
    min_val: float = 0
    max_val: float = 100
    num_vals: int = 1  # Number of values to generate
    jitter: bool = True  # Whether to add some noise to the values
    algorithm: FakeMetricAlgorithms = FakeMetricAlgorithms.LINEAR_SYNCED


# TODO: Write tests once useful.
class FakeMetricGenerator:
    """ Generate fake values for metrics, with support for cyclic and random patterns."""
    def __init__(self, config: FakeMetricConfig):
        self.config = config
        self.start_time = time.time()

    def sample(self, override_elapsed: float | None = None) -> list[float]:
        # override_elapsed allows us to force it to generate a value based on a fake elapsed
        # time. This is ONLY for testing.

        if override_elapsed:
            elapsed = override_elapsed
        else:
            elapsed = time.time() - self.start_time

        sample_point = elapsed % self.config.period
        if self.config.algorithm == FakeMetricAlgorithms.LINEAR_SYNCED:
            vals = self._generate_linear(sample_point)
        elif self.config.algorithm == FakeMetricAlgorithms.RANDOM:
            vals = self._generate_random(sample_point)
        else:
            raise RuntimeError("This should be impossible unless I forgot to handle a new AlgorithmType")
        return vals

    def _generate_random(self, sample_point: float) -> list[float]:
        # sample_point is ignored. Jitter is ignored.
        vals = [
            random.uniform(self.config.min_val, self.config.max_val)
            for _ in range(self.config.num_vals)
        ]
        return vals

    def _generate_linear(self, sample_point: float):
        # sample_point is ignored. Jitter is ignored.
        percent = sample_point / self.config.period
        val_range = self.config.max_val - self.config.min_val
        assert val_range >= 0, "max_val must be greater than or equal to min_val"
        delta = percent * val_range
        pre_jitter_val = self.config.min_val + delta
        # Vary by up to ±10% and then bound by min and max
        if self.config.jitter:
            jitter_deltas = [
                random.uniform(-0.1, 0.1) * pre_jitter_val
                for _ in range(self.config.num_vals)
            ]
        else:
            jitter_deltas = [0 for _ in range(self.config.num_vals)]

        jittered_vals = [pre_jitter_val + jitter_delta for jitter_delta in jitter_deltas]
        # Bound by min and max
        final_vals = [
            min(max(jittered_val, self.config.min_val), self.config.max_val)
            for jittered_val in jittered_vals
        ]
        return final_vals


if __name__ == '__main__':
    def pretty_float(num: float):
        pretty_val = "{0:,.2f}".format(num)
        if len(pretty_val) == 4:
            pretty_val = f"0{pretty_val}"
        return pretty_val

    config = FakeMetricConfig(num_vals=4, jitter=False, algorithm=FakeMetricAlgorithms.RANDOM)
    generator = FakeMetricGenerator(config)
    start_time = time.time()
    while True:
        vals = generator.sample()
        elapsed_secs_str = pretty_float(time.time() - start_time)
        pretty_vals = [pretty_float(val) for val in vals]
        print(f"{elapsed_secs_str}: {pretty_vals}")
        time.sleep(1)

