import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class GpuUtilizationVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_gpu_util"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # util example: [20, 40, 60, 80]
    gpu_percents: Mapped[list[float]] = mapped_column(JSONB, nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class GpuUtilizationVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_gpu_util_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # util example: [20, 40, 60, 80]
    gpu_percents: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class GpuUtilizationVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    gpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: GpuUtilizationVmMetricORM) -> "GpuUtilizationVmMetric":
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            gpu_percents=orm.gpu_percents,
        )


class GpuUtilizationVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    gpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: GpuUtilizationVmMetricORM) -> "GpuUtilizationVmMetricLatest":
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            gpu_percents=orm.gpu_percents,
        )
