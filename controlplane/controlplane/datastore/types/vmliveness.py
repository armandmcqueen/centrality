import datetime
from pydantic import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM


class VmHeartbeatORM(DatastoreBaseORM):
    __tablename__ = "vm_heartbeat"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    last_heartbeat_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )



class VmHeartbeat(BaseModel):
    vm_id: str
    last_heartbeat_ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: VmHeartbeatORM) -> "VmHeartbeat":
        return cls(
            vm_id=orm.vm_id,
            last_heartbeat_ts=orm.last_heartbeat_ts,
        )
