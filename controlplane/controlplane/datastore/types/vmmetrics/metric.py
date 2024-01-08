import datetime
from pydantic import BaseModel
from typing import Any


from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid
from typing import TypeVar, Type, Generic


# TODO: This code was created when I was trying to reduce duplicated code via inheritance. I've moved
#   to doing this via code generation instead. Some of the code in this file can probably be deleted/
#   moved into codegen. But the code works fine for now.

# Define a type variable that can be any subclass of MetricBaseModel
T1 = TypeVar("T1", bound="MetricBaseModel")
T2 = TypeVar("T2", bound="MetricLatestBaseModel")


class MetricLatestBaseORM(DatastoreBaseORM):
    __abstract__ = True

    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    # Overwrite this in subclasses for type safety
    metrics: Mapped[Any] = mapped_column(JSONB, nullable=False)


class MetricBaseORM(DatastoreBaseORM):
    __abstract__ = True

    metric_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    vm_id: Mapped[str] = mapped_column(primary_key=False, nullable=False)
    ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    # Overwrite this in subclasses for type safety
    metrics: Mapped[Any] = mapped_column(JSONB, nullable=False)


class MetricBaseModel(BaseModel, Generic[T1]):
    metric_id: str
    vm_id: str
    ts: datetime.datetime

    @classmethod
    def from_orm(cls: Type[T1], orm: MetricBaseORM, **kwargs) -> T1:
        return cls(
            metric_id=orm.metric_id,
            vm_id=orm.vm_id,
            ts=orm.ts,
            **kwargs,  # Pass additional keyword arguments to the constructor
        )


class MetricLatestBaseModel(BaseModel, Generic[T2]):
    vm_id: str
    ts: datetime.datetime

    @classmethod
    def from_orm(cls: Type[T2], orm: MetricLatestBaseORM, **kwargs) -> T2:
        return cls(
            vm_id=orm.vm_id,
            ts=orm.ts,
            **kwargs,  # Pass additional keyword arguments to the constructor
        )
