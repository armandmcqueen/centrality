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
from pydantic import BaseModel, Field


metric_name = "disk_throughput"
# example disk_throughput metrics: {disk1: [read, write], disk2: [read, write]}
metric_shape_db = dict[str, list[float]]


# Custom Types
class DiskThroughput(BaseModel):
    disk_name: str = Field(..., description="The name of the disk, e.g. /dev/sda.")
    read_mbps: float = Field(
        ..., description="The read throughput for the disk in MiB/s."
    )
    write_mbps: float = Field(
        ..., description="The write throughput for the disk in MiB/s."
    )


# Convert metrics column in DB to object fields as dict that can be passed to super().from_orm() as kwargs
def convert_from_metrics(
    metrics: dict[str, list[float]],
) -> dict[str, list[DiskThroughput]]:
    throughput: list[DiskThroughput] = [
        DiskThroughput(
            disk_name=disk, read_mbps=throughput_vals[0], write_mbps=throughput_vals[1]
        )
        for disk, throughput_vals in metrics.items()
    ]
    return dict(throughput=throughput)


# Convert user-facing object fields to metrics column shape in DB
def convert_to_metrics(self: Any) -> dict[str, list[float]]:
    return {
        throughput.disk_name: [throughput.read_mbps, throughput.write_mbps]
        for throughput in self.throughput
    }


class DiskThroughputMetricLatestORM(MetricLatestBaseORM):
    __tablename__ = "machine_metric_disk_throughput_latest"
    metrics: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)


class DiskThroughputMetricORM(MetricBaseORM):
    __tablename__ = "machine_metric_disk_throughput"
    metrics: Mapped[dict[str, list[float]]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("idx_metric_disk_throughput_ts", "ts"),  # Creating the index
        Index(
            "idx_metric_disk_throughput_machine_id_ts", "machine_id", "ts"
        ),  # Composite index
    )


class DiskThroughputMetricLatest(MetricLatestBaseModel):
    machine_id: str
    ts: datetime.datetime
    throughput: list[DiskThroughput] = Field(
        ...,
        description="A list with disk throughput for each disk. Each disk will have one entry in the list.",
    )

    @classmethod
    def from_orm(
        cls, orm: DiskThroughputMetricLatestORM, **kwargs
    ) -> "DiskThroughputMetricLatest":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(DiskThroughputMetricLatest, instance)

    def to_disk_throughput_measurement(self) -> "DiskThroughputMeasurement":
        kwargs = self.model_dump()
        return DiskThroughputMeasurement(**kwargs)


class DiskThroughputMetric(MetricBaseModel):
    metric_id: str
    machine_id: str
    ts: datetime.datetime
    throughput: list[DiskThroughput] = Field(
        ...,
        description="A list with disk throughput for each disk. Each disk will have one entry in the list.",
    )

    @classmethod
    def from_orm(cls, orm: DiskThroughputMetricORM, **kwargs) -> "DiskThroughputMetric":
        instance = super().from_orm(orm=orm, **convert_from_metrics(orm.metrics))
        return cast(DiskThroughputMetric, instance)

    def to_disk_throughput_measurement(self) -> "DiskThroughputMeasurement":
        kwargs = self.model_dump()
        kwargs.pop("metric_id")
        return DiskThroughputMeasurement(**kwargs)


class DiskThroughputMeasurement(BaseModel):
    """
    A measurement of DiskThroughput
    """

    # This is the user-facing object that is sent to and from the REST endpoint
    machine_id: str = Field(
        ..., description="The machine_id of the machine that generated this measurement"
    )
    ts: datetime.datetime = Field(..., description="The timestamp of the measurement")
    throughput: list[DiskThroughput] = Field(
        ...,
        description="A list with disk throughput for each disk. Each disk will have one entry in the list.",
    )

    def to_metrics(self) -> dict[str, list[float]]:
        return convert_to_metrics(self)
