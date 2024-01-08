from typing import cast

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)

# example: [cpuWWW, cpuXXX, cpuYYY, cpuZZZ]
METRIC_SHAPE_DB = list[float]
METRIC_NAME = "cpu"


class CpuMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}_latest"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class CpuMetricORM(MetricBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class CpuMetricLatest(MetricLatestBaseModel):
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricLatestORM, **kwargs) -> "CpuMetricLatest":
        instance = super().from_orm(orm=orm, cpu_percents=orm.metrics)
        return cast(CpuMetricLatest, instance)


class CpuMetric(MetricBaseModel):
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuMetricORM, **kwargs) -> "CpuMetric":
        instance = super().from_orm(orm=orm, cpu_percents=orm.metrics)
        return cast(CpuMetric, instance)
