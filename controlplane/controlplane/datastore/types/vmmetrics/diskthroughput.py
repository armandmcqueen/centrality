import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class DiskThroughput(BaseModel):
    read_mbps: float
    write_mbps: float


class DiskThroughputVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_throughput"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # disk_throughput example: {disk1: [read, write], disk2: [read, write]}
    disk_throughput: Mapped[dict[str, list[float]]] = mapped_column(
        JSONB, nullable=False
    )
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class DiskThroughputVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_disk_throughput_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # throughputs example: {disk1: [read, write], disk2: [read, write]}
    throughputs: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)


class DiskThroughputVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    throughputs: dict[str, DiskThroughput]

    @classmethod
    def from_orm(cls, orm: DiskThroughputVmMetricORM) -> "DiskThroughputVmMetric":
        throughputs = {
            disk: DiskThroughput(read_mbps=throughput[0], write_mbps=throughput[1])
            for disk, throughput in orm.disk_throughput.items()
        }
        return cls(
            metric_id=orm.metric_id, vm_id=orm.vm_id, ts=orm.ts, throughputs=throughputs
        )


class DiskThroughputVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    throughputs: dict[str, DiskThroughput]

    @classmethod
    def from_orm(
        cls, orm: DiskThroughputVmMetricLatestORM
    ) -> "DiskThroughputVmMetricLatest":
        throughputs = {
            disk: DiskThroughput(read_mbps=throughput[0], write_mbps=throughput[1])
            for disk, throughput in orm.throughputs.items()
        }
        return cls(vm_id=orm.vm_id, ts=orm.ts, throughputs=throughputs)
