import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class DiskUsage(BaseModel):
    used_mb: float
    total_mb: float


class DiskUsageVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_usage"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # disk_usage example: {disk1: [used, total], disk2: [used, total]}
    usage: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class DiskUsageVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_usage_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # disk_usage example: {disk1: [used, total], disk2: [used, total]}
    usage: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)


class DiskUsageVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    usage: dict[str, DiskUsage]

    @classmethod
    def from_orm(cls, orm: DiskUsageVmMetricORM) -> "DiskUsageVmMetric":
        usage = {
            disk: DiskUsage(used_mb=usage_vals[0], total_mb=usage_vals[1])
            for disk, usage_vals in orm.usage.items()
        }
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            usage=usage,
        )


class DiskUsageVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    usage: dict[str, DiskUsage]

    @classmethod
    def from_orm(cls, orm: DiskUsageVmMetricLatestORM) -> "DiskUsageVmMetricLatest":
        usage = {
            disk: DiskUsage(used_mb=usage_vals[0], total_mb=usage_vals[1])
            for disk, usage_vals in orm.usage.items()
        }
        return cls(vm_id=orm.vm_id, ts=orm.ts, usage=usage)
