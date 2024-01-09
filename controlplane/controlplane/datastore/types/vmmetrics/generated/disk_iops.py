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


metric_name = "disk_iops"
# example disk_iops metrics: {disk1: iopsXXX, disk2: iopsYYY}
metric_shape_db = dict[str, float]


# Custom Types
class DiskIops(BaseModel):
    disk_name: str
    iops: float


# Convert metrics column in DB to object fields as dict that can be passed to super().from_orm() as kwargs
def convert_from_metrics(metrics: dict[str, float]) -> dict[str, list[DiskIops]]:
    iops: list[DiskIops] = [
        DiskIops(disk_name=device, iops=iops_val)
        for device, iops_val in metrics.items()
    ]
    return dict(iops=iops)


# Convert user-facing object fields to metrics column shape in DB
def convert_to_metrics(self: Any) -> dict[str, float]:
    iops = {}
    for iop in self.iops:
        iops[iop.disk_name] = iop.iops
    return iops


class DiskIopsMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_disk_iops_latest"
    metrics: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)


class DiskIopsMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_disk_iops"
    metrics: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metric_disk_iops_ts", "ts"),  # Creating the index
        Index("idx_metric_disk_iops_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class DiskIopsMetricLatest(MetricLatestBaseModel):
    vm_id: str
    ts: datetime.datetime
    iops: list[DiskIops]

    @classmethod
    def from_orm(cls, orm: DiskIopsMetricLatestORM, **kwargs) -> "DiskIopsMetricLatest":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(DiskIopsMetricLatest, instance)

    def to_disk_iops_measurement(self) -> "DiskIopsMeasurement":
        kwargs = self.model_dump()
        return DiskIopsMeasurement(**kwargs)


class DiskIopsMetric(MetricBaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    iops: list[DiskIops]

    @classmethod
    def from_orm(cls, orm: DiskIopsMetricORM, **kwargs) -> "DiskIopsMetric":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(DiskIopsMetric, instance)

    def to_disk_iops_measurement(self) -> "DiskIopsMeasurement":
        kwargs = self.model_dump()
        kwargs.pop("metric_id")
        return DiskIopsMeasurement(**kwargs)


class DiskIopsMeasurement(BaseModel):
    """
    A measurement of DiskIops
    """

    # This is the user-facing object that is sent to and from the REST endpoint
    vm_id: str
    ts: datetime.datetime
    iops: list[DiskIops]

    def to_metrics(self) -> dict[str, float]:
        return convert_to_metrics(self)
