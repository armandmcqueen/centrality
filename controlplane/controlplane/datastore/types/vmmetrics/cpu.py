import datetime
from pydantic import BaseModel
from typing import List

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class CpuVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_cpu"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    cpu_percents: Mapped[List[float]] = mapped_column(JSONB, nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class CpuVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_cpu_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    cpu_percents: Mapped[list[float]] = mapped_column(JSONB, nullable=False)


class CpuVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    cpu_percents: list[float]

    @classmethod
    def from_orm(cls, orm: CpuVmMetricORM) -> "CpuVmMetric":
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            cpu_percents=orm.cpu_percents,
        )


class CpuVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    cpu_percents: List[float]

    @classmethod
    def from_orm(cls, orm: CpuVmMetricLatestORM) -> "CpuVmMetricLatest":
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            cpu_percents=orm.cpu_percents,
        )
