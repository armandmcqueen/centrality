import datetime
from pydantic import BaseModel
from typing import List

from common.types.vmmetrics import CpuMeasurement


from sqlalchemy import ARRAY, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


#######################################################
# Example of how to add a new metric to the datastore #
#######################################################

# class ExampleVmMetricORM(DatastoreBaseORM):
#     __tablename__ = "vm_metric_example"
#     metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
#     vm_id: Mapped[str] = mapped_column(nullable=False)
#     ts: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
#
#
# @dataclass
# class ExampleVmMetric(BaseModel):
#     metric_id: str
#     vm_id: str
#     ts: datetime.datetime


class CpuVmMetricORM(DatastoreBaseORM):
    __tablename__ = "vm_metric_cpu"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # cpu_percents: Mapped[List[float]] = mapped_column(nullable=False)
    cpu_percents: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)
    avg_cpu_percent: Mapped[float] = mapped_column(nullable=False)


class CpuVmMetric(BaseModel):
    # Is this useful? It has overlap with the type in common/types/vmmetrics.py, but
    # includes some additional info that maybe shouldn't be exposed to users?
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    cpu_percents: List[float]
    avg_cpu_percent: float

    @classmethod
    def from_orm(cls, orm: CpuVmMetricORM) -> "CpuVmMetric":
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            cpu_percents=orm.cpu_percents,
            avg_cpu_percent=orm.avg_cpu_percent,
        )
