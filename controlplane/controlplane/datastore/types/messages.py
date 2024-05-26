from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid
import datetime
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sqlalchemy.orm import Mapped, mapped_column


class MachineAgentMessageORM(DatastoreBaseORM):
    __tablename__ = "machine_agent_messages"

    msg_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    creation_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    machine_id: Mapped[str] = mapped_column(nullable=False)
    is_ask: Mapped[bool] = mapped_column(nullable=False)
    msg_type: Mapped[str] = mapped_column(nullable=False)
    msg_content: Mapped[str] = mapped_column(nullable=False)
    msg_state: Mapped[str] = mapped_column(
        nullable=False, default="SENT"
    )  # TODO: Enum? SENT | ACKD | COMPLETE
    errored: Mapped[bool] = mapped_column(nullable=False, default=False)
    outcome: Mapped[str] = mapped_column(nullable=False, default="")
    max_response_chars: Mapped[int] = mapped_column(nullable=False)
    timeout_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )


class MachineAgentMessage(BaseModel):
    msg_id: str
    creation_ts: datetime.datetime
    machine_id: str
    is_ask: bool
    msg_type: str
    msg_content: str
    msg_state: str
    errored: bool
    outcome: str
    max_response_chars: int
    timeout_ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: MachineAgentMessageORM) -> "MachineAgentMessage":
        return cls(
            msg_id=orm.msg_id,
            creation_ts=orm.creation_ts,
            machine_id=orm.machine_id,
            is_ask=orm.is_ask,
            msg_type=orm.msg_type,
            msg_content=orm.msg_content,
            msg_state=orm.msg_state,
            errored=orm.errored,
            outcome=orm.outcome,
            max_response_chars=orm.max_response_chars,
            timeout_ts=orm.timeout_ts,
        )


class MachineAgentMessageCreationInfo(BaseModel):
    machine_id: str
    is_ask: bool
    msg_type: str
    msg_content: str
    max_response_chars: int


class MachineAgentMessageCompletionInfo(BaseModel):
    msg_id: str
    errored: bool
    outcome: str
