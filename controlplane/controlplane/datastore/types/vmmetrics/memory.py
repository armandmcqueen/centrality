import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class MemoryVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_memory"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    free_memory_mb: Mapped[float] = mapped_column(nullable=False)
    total_memory_mb: Mapped[float] = mapped_column(nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class MemoryVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_memory_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    free_memory_mb: Mapped[float] = mapped_column(nullable=False)
    total_memory_mb: Mapped[float] = mapped_column(nullable=False)


class MemoryVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    free_memory_mb: float
    total_memory_mb: float

    @classmethod
    def from_orm(cls, orm: MemoryVmMetricORM) -> "MemoryVmMetric":
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            free_memory_mb=orm.free_memory_mb,
            total_memory_mb=orm.total_memory_mb,
        )


class MemoryVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    free_memory_mb: float
    total_memory_mb: float

    @classmethod
    def from_orm(cls, orm: MemoryVmMetricLatestORM) -> "MemoryVmMetricLatest":
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            free_memory_mb=orm.free_memory_mb,
            total_memory_mb=orm.total_memory_mb,
        )
