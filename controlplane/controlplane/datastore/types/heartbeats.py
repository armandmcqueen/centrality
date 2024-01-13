import datetime
from pydantic import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM


# TODO: Add to sweeper
class MachineHeartbeatsOrm(DatastoreBaseORM):
    __tablename__ = "machine_heartbeats"
    heartbeat_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    machine_id: Mapped[str] = mapped_column(nullable=False)
    heartbeat_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )


class MachineHeartbeat(BaseModel):
    """
    A single machine heartbeat
    """

    # IMPORTANT: If you change this, you must also change the MachineRegistration class below
    heartbeat_id: str
    machine_id: str
    heartbeat_ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: MachineHeartbeatsOrm) -> "MachineHeartbeat":
        return cls(
            heartbeat_id=orm.heartbeat_id,
            machine_id=orm.machine_id,
            heartbeat_ts=orm.heartbeat_ts,
        )

    def to_orm(self) -> MachineHeartbeatsOrm:
        return MachineHeartbeatsOrm(
            heartbeat_id=self.heartbeat_id,
            machine_id=self.machine_id,
            heartbeat_ts=self.heartbeat_ts,
        )
