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


metric_name = "cpu"
# example cpu metrics: [cpuWWW, cpuXXX, cpuYYY, cpuZZZ]
metric_shape_db = list[float]


# Custom Types
CpuPercents = list[float]


# Convert metrics column in DB to object fields as dict that can be passed to super().from_orm() as kwargs
def convert_from_metrics(metrics: list[float]) -> dict[str, CpuPercents]:
    return dict(cpu_percents=metrics)


# Convert user-facing object fields to metrics column shape in DB
def convert_to_metrics(self: Any) -> list[float]:
    return self.cpu_percents


class CpuMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_cpu_latest"
    metrics: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class CpuMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_cpu"
    metrics: Mapped[list[float]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metric_cpu_ts", "ts"),  # Creating the index
        Index("idx_metric_cpu_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class CpuMetricLatest(MetricLatestBaseModel):
    vm_id: str
    ts: datetime.datetime
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricLatestORM, **kwargs) -> "CpuMetricLatest":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(CpuMetricLatest, instance)

    def to_cpu_measurement(self) -> "CpuMeasurement":
        kwargs = self.model_dump()
        return CpuMeasurement(**kwargs)


class CpuMetric(MetricBaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricORM, **kwargs) -> "CpuMetric":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(CpuMetric, instance)

    def to_cpu_measurement(self) -> "CpuMeasurement":
        kwargs = self.model_dump()
        kwargs.pop("metric_id")
        return CpuMeasurement(**kwargs)


class CpuMeasurement(BaseModel):
    """
    A measurement of Cpu
    """

    # This is the user-facing object that is sent to and from the REST endpoint
    vm_id: str
    ts: datetime.datetime
    cpu_percents: list[float]

    def to_metrics(self) -> list[float]:
        return convert_to_metrics(self)
