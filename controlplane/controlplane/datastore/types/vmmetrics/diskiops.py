from typing import cast

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)

# example: {disk1: iops, disk2: iops}
METRIC_SHAPE_DB = dict[str, float]
METRIC_NAME = "disk_iops"


class DiskIopsMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}_latest"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class DiskIopsMetricORM(MetricBaseORM):
    __tablename__ = f"machine_metric_{METRIC_NAME}"
    metrics: Mapped[METRIC_SHAPE_DB] = mapped_column(JSONB, nullable=False)


class DiskIopsMetricLatest(MetricLatestBaseModel):
    iops: METRIC_SHAPE_DB

    @classmethod
    def from_orm(cls, orm: DiskIopsMetricLatestORM, **kwargs) -> "DiskIopsMetricLatest":
        instance = super().from_orm(orm=orm, iops=orm.metrics)
        return cast(DiskIopsMetricLatest, instance)


class DiskIopsMetric(MetricBaseModel):
    iops: METRIC_SHAPE_DB

    @classmethod
    def from_orm(cls, orm: DiskIopsMetricORM, **kwargs) -> "DiskIopsMetric":
        instance = super().from_orm(orm=orm, iops=orm.metrics)
        return cast(DiskIopsMetric, instance)
