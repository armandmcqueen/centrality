import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class GpuMemoryVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_gpu_memory"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # memory example: [[used, total], [used, total]]
    utilization: Mapped[list[float]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class GpuMemoryVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_gpu_memory_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    # memory example: [[used, total], [used, total]]
    utilization: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class GpuMemory(BaseModel):
    used_mb: float
    total_mb: float


class GpuMemoryVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    memory: list[GpuMemory]

    @classmethod
    def from_orm(cls, orm: GpuMemoryVmMetricORM) -> "GpuMemoryVmMetric":
        memory = [
            GpuMemory(used_mb=usage[0], total_mb=usage[1]) for usage in orm.utilization
        ]
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            memory=memory,
        )


class GpuMemoryVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    memory: list[GpuMemory]

    @classmethod
    def from_orm(cls, orm: GpuMemoryVmMetricORM) -> "GpuMemoryVmMetricLatest":
        memory = [
            GpuMemory(used_mb=usage[0], total_mb=usage[1]) for usage in orm.utilization
        ]
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            memory=memory,
        )
