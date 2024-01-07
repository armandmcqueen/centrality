import datetime
from pydantic import BaseModel

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid


class NetworkThroughputVmMetricORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_network_throughput"
    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # throughput example: {ifaceA: [sentXXX, recvXXX], ifaceB: [sentYYY, recvYYY], total: [sentZZZ, recvZZZ]}
    throughput: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)
    __table_args__ = (
        Index("idx_metrics_ts", "ts"),  # Creating the index
        Index("idx_vm_id_ts", "vm_id", "ts"),  # Composite index
    )


class MemoryVmMetricLatestORM(DatastoreBaseORM):
    __tablename__ = "machine_metric_network_throughput_latest"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # throughput example: {ifaceA: [sentXXX, recvXXX], ifaceB: [sentYYY, recvYYY], total: [sentZZZ, recvZZZ]}
    throughput: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)


class Throughput(BaseModel):
    sent_mbps: float
    recv_mbps: float


class NetworkThroughputVmMetric(BaseModel):
    metric_id: str
    vm_id: str
    ts: datetime.datetime
    per_interface: dict[str, Throughput]
    total: Throughput

    @classmethod
    def from_orm(cls, orm: NetworkThroughputVmMetricORM) -> "NetworkThroughputVmMetric":
        interfaces = {
            interface: Throughput(sent_mbps=throughput[0], recv_mbps=throughput[1])
            for interface, throughput in orm.throughput.items()
            if interface != "total"
        }
        # TODO: Test this works?
        total = Throughput(
            sent_mbps=orm.throughput["total"][0], recv_mbps=orm.throughput["total"][1]
        )
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            per_interface=interfaces,
            total=total,
        )


class NetworkThroughputVmMetricLatest(BaseModel):
    vm_id: str
    ts: datetime.datetime
    per_interface: dict[str, Throughput]
    total: Throughput

    @classmethod
    def from_orm(
        cls, orm: NetworkThroughputVmMetricORM
    ) -> "NetworkThroughputVmMetricLatest":
        interfaces = {
            interface: Throughput(sent_mbps=throughput[0], recv_mbps=throughput[1])
            for interface, throughput in orm.throughput.items()
            if interface != "total"
        }
        # TODO: Test this works?
        total = Throughput(
            sent_mbps=orm.throughput["total"][0], recv_mbps=orm.throughput["total"][1]
        )
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            per_interface=interfaces,
            total=total,
        )
