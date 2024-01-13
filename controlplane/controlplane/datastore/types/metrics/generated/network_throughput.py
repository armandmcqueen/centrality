# AUTOGENERATED FILE DO NOT EDIT

from typing import cast, Any
import datetime
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from controlplane.datastore.types.metrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)
from pydantic import BaseModel


metric_name = "network_throughput"
# example network_throughput metrics: {ifaceA: [sentXXX, recvXXX], ifaceB: [sentYYY, recvYYY], total: [sentZZZ, recvZZZ]}
metric_shape_db = dict[str, list[float]]


# Custom Types
class Throughput(BaseModel):
    interface_name: str
    sent_mbps: float
    recv_mbps: float


# Convert metrics column in DB to object fields as dict that can be passed to super().from_orm() as kwargs
def convert_from_metrics(
    metrics: dict[str, list[float]],
) -> dict[str, list[Throughput] | Throughput]:
    interfaces: list[Throughput] = [
        Throughput(
            interface_name=interface, sent_mbps=throughput[0], recv_mbps=throughput[1]
        )
        for interface, throughput in metrics.items()
        if interface != "total"
    ]
    total = Throughput(
        interface_name="total",
        sent_mbps=metrics["total"][0],
        recv_mbps=metrics["total"][1],
    )
    return dict(per_interface=interfaces, total=total)


# Convert user-facing object fields to metrics column shape in DB
def convert_to_metrics(self: Any) -> dict[str, list[float]]:
    return {
        throughput.interface_name: [throughput.sent_mbps, throughput.recv_mbps]
        for throughput in self.per_interface
    }


class NetworkThroughputMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_network_throughput_latest"
    metrics: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)


class NetworkThroughputMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_network_throughput"
    metrics: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metric_network_throughput_ts", "ts"),  # Creating the index
        Index(
            "idx_metric_network_throughput_machine_id_ts", "machine_id", "ts"
        ),  # Composite index
    )


class NetworkThroughputMetricLatest(MetricLatestBaseModel):
    machine_id: str
    ts: datetime.datetime
    per_interface: list[Throughput]
    total: Throughput

    @classmethod
    def from_orm(
        cls, orm: NetworkThroughputMetricLatestORM, **kwargs
    ) -> "NetworkThroughputMetricLatest":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(NetworkThroughputMetricLatest, instance)

    def to_network_throughput_measurement(self) -> "NetworkThroughputMeasurement":
        kwargs = self.model_dump()
        return NetworkThroughputMeasurement(**kwargs)


class NetworkThroughputMetric(MetricBaseModel):
    metric_id: str
    machine_id: str
    ts: datetime.datetime
    per_interface: list[Throughput]
    total: Throughput

    @classmethod
    def from_orm(
        cls, orm: NetworkThroughputMetricORM, **kwargs
    ) -> "NetworkThroughputMetric":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(NetworkThroughputMetric, instance)

    def to_network_throughput_measurement(self) -> "NetworkThroughputMeasurement":
        kwargs = self.model_dump()
        kwargs.pop("metric_id")
        return NetworkThroughputMeasurement(**kwargs)


class NetworkThroughputMeasurement(BaseModel):
    """
    A measurement of NetworkThroughput
    """

    # This is the user-facing object that is sent to and from the REST endpoint
    machine_id: str
    ts: datetime.datetime
    per_interface: list[Throughput]
    total: Throughput

    def to_metrics(self) -> dict[str, list[float]]:
        return convert_to_metrics(self)