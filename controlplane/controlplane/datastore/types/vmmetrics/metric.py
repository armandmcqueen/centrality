import datetime
from pydantic import BaseModel
from typing import Any

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class MetricLatestBaseORM(DatastoreBaseORM):
    __tablename__ = "base_metric_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # Overwrite this in subclasses for type safety
    metrics: Mapped[Any] = mapped_column(JSONB, nullable=False)


class MetricBaseORM(DatastoreBaseORM):
    __tablename__ = "base_metric"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )

    # Overwrite this in subclasses for type safety
    metrics: Mapped[Any] = mapped_column(JSONB, nullable=False)


class MetricBaseModel(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: MetricBaseORM, **kwargs):
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            **kwargs,  # Pass additional keyword arguments to the constructor
        )


class MetricLatestBaseModel(BaseModel):
    vm_id: str
    ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: MetricLatestBaseORM, **kwargs) -> "MetricLatestBaseModel":
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            **kwargs,  # Pass additional keyword arguments to the constructor
        )
