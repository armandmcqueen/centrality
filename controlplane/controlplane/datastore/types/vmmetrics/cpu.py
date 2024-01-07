from typing import cast

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)


class CpuMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_cpu"
    metrics: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class CpuMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_cpu_latest"
    metrics: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class CpuMetric(MetricBaseModel):
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricORM) -> "CpuMetric":  # noqa
        instance = super().from_orm(orm, cpu_percents=orm.metrics)
        return cast(CpuMetric, instance)


class CpuMetricLatest(MetricLatestBaseModel):
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricLatestORM) -> "CpuMetricLatest":  # noqa
        instance = super().from_orm(orm, cpu_percents=orm.metrics)
        return cast(CpuMetricLatest, instance)
