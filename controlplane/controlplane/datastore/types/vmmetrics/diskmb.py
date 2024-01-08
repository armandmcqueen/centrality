from typing import cast

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)


class DiskUsage(BaseModel):
    used_mb: float
    total_mb: float


# example: {disk1: [used, total], disk2: [used, total]}
METRIC_SHAPE_DB = dict[str, list[float]]
METRIC_SHAPE_OBJ = dict[str, DiskUsage]
METRIC_NAME = "disk_usage"


def convert(metric: METRIC_SHAPE_DB) -> METRIC_SHAPE_OBJ:
    return {
        disk: DiskUsage(used_mb=usage_vals[0], total_mb=usage_vals[1])
        for disk, usage_vals in metric.items()
    }


class DiskUsageMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}_latest"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class DiskUsageMetricORM(MetricBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class DiskUsageMetricLatest(MetricLatestBaseModel):
    usage: METRIC_SHAPE_OBJ

    @classmethod
    def from_orm(
        cls, orm: DiskUsageMetricLatestORM, **kwargs
    ) -> "DiskUsageMetricLatest":
        instance = super().from_orm(orm=orm, usage=convert(orm.metrics))
        return cast(DiskUsageMetricLatest, instance)


class DiskUsageMetric(MetricBaseModel):
    usage: METRIC_SHAPE_OBJ

    @classmethod
    def from_orm(cls, orm: DiskUsageMetricORM, **kwargs) -> "DiskUsageMetric":
        instance = super().from_orm(orm=orm, usage=convert(orm.metrics))
        return cast(DiskUsageMetric, instance)
