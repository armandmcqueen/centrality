import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class DiskIopsVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_iops"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # iops example: {dist1: iops, disk2: iops}
    iops: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class DiskIopsVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_iops_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # iops example: {dist1: iops, disk2: iops}
    iops: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)


class DiskIopsVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    iops: dict[str, float]

    @classmethod
    def from_orm(cls, orm: DiskIopsVmMetricORM) -> "DiskIopsVmMetric":
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            iops=orm.iops,
        )


class DiskIopsVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    iops: dict[str, float]

    @classmethod
    def from_orm(cls, orm: DiskIopsVmMetricLatestORM) -> "DiskIopsVmMetricLatest":
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            iops=orm.iops,
        )
