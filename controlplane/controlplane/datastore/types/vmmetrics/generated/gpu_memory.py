# AUTOGENERATED FILE DO NOT EDIT

from typing import cast, Any
import datetime
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)
from pydantic import BaseModel


metric_name = "gpu_memory"
# example gpu_memory metrics: [[used, total], [used, total]]
metric_shape_db = list[list[float]]


# Custom Types
class GpuMemory(BaseModel):
    used_mb: float
    total_mb: float


# Convert metrics column in DB to object fields as dict that can be passed to super().from_orm() as kwargs
def convert_from_metrics(metrics: list[list[float]]) -> dict[str, list[GpuMemory]]:
    memory = [
        GpuMemory(used_mb=memory_vals[0], total_mb=memory_vals[1])
        for memory_vals in metrics
    ]

    return dict(memory=memory)


# Convert user-facing object fields to metrics column shape in DB
def convert_to_metrics(self: Any) -> list[list[float]]:
    return [[memory.used_mb, memory.total_mb] for memory in self.memory]


class GpuMemoryMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_gpu_memory_latest"
    metrics: Mapped[list[list[float]]] = mapped_column(JSONB, nullable=False)


class GpuMemoryMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_gpu_memory"
    metrics: Mapped[list[list[float]]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metric_gpu_memory_ts", "ts"),  # Creating the index
        Index("idx_metric_gpu_memory_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class GpuMemoryMetricLatest(MetricLatestBaseModel):
    vm_id: str
    ts: datetime.datetime
    memory: list[GpuMemory]

    @classmethod
    def from_orm(
        cls, orm: GpuMemoryMetricLatestORM, **kwargs
    ) -> "GpuMemoryMetricLatest":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(GpuMemoryMetricLatest, instance)

    def to_gpu_memory_measurement(self) -> "GpuMemoryMeasurement":
        kwargs = self.model_dump()
        return GpuMemoryMeasurement(**kwargs)


class GpuMemoryMetric(MetricBaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    memory: list[GpuMemory]

    @classmethod
    def from_orm(cls, orm: GpuMemoryMetricORM, **kwargs) -> "GpuMemoryMetric":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(GpuMemoryMetric, instance)

    def to_gpu_memory_measurement(self) -> "GpuMemoryMeasurement":
        kwargs = self.model_dump()
        kwargs.pop("metric_id")
        return GpuMemoryMeasurement(**kwargs)


class GpuMemoryMeasurement(BaseModel):
    """
    A measurement of GpuMemory
    """

    # This is the user-facing object that is sent to and from the REST endpoint
    vm_id: str
    ts: datetime.datetime
    memory: list[GpuMemory]

    def to_metrics(self) -> list[list[float]]:
        return convert_to_metrics(self)