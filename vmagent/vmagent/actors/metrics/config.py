from common.config.config import CentralityConfig
from actors.metrics.faketrics import FakeMetricConfig
from pydantic import Field


class CpuMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(num_vals=16)  # 16 CPUs
    )


class MemoryMetricConfig(CentralityConfig):
    """
    fake.num_vals must be 1 for MemoryMetricCollector - there's only one memory metric!
    """

    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(num_vals=1, max_val=16_000)  # 16 GiB
    )


class NetworkMetricConfig(CentralityConfig):
    """
    fake.num_vals must be 1 for NetworkMetricCollector - we don't support more complex simulation yet.
    """

    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(
            num_vals=1, max_val=12_500
        )  # 12.5 GByte/s == 100 Gbit/s
    )


class DiskIoMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(
            num_vals=2, max_val=500
        )  # 2 disks, 500 IOPS and 500 MiB/s read and write
    )


class DiskMbMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(
            num_vals=2, max_val=500_000
        )  # 2 disks, 500 GiB
    )


class GpuUtilMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(num_vals=8)  # 8 GPU
    )


class GpuMemMetricConfig(CentralityConfig):
    use_fake: bool = False
    fake: FakeMetricConfig = Field(
        default_factory=lambda: FakeMetricConfig(
            num_vals=8, max_val=64_000
        )  # 8 GPU, 64 GiB
    )


class MetricsConfig(CentralityConfig):
    cpu: CpuMetricConfig = Field(default_factory=CpuMetricConfig)
    diskio: DiskIoMetricConfig = Field(default_factory=DiskIoMetricConfig)
    diskmb: DiskMbMetricConfig = Field(default_factory=DiskMbMetricConfig)
    gpuutil: GpuUtilMetricConfig = Field(default_factory=GpuUtilMetricConfig)
    gpumem: GpuMemMetricConfig = Field(default_factory=GpuMemMetricConfig)
    memory: MemoryMetricConfig = Field(default_factory=MemoryMetricConfig)
    network: NetworkMetricConfig = Field(default_factory=NetworkMetricConfig)
