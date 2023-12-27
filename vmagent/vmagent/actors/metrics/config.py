from common.config.config import CentralityConfig
from vmagent.actors.metrics.faketrics import FakeMetricConfig
from pydantic import Field


class CpuMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(num_vals=16)
    )


class MetricsConfig(CentralityConfig):
    cpu: CpuMetricConfig = Field(default_factory=CpuMetricConfig)
