import datetime
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM


class PreviewBranchStateORM(DatastoreBaseORM):
    __tablename__ = "preview_branch_state"
    branch_name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    deployed_commit: Mapped[Optional[str]] = mapped_column(nullable=True)
    last_update_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )


class PreviewBranchState(BaseModel):
    branch_name: str
    is_active: bool
    deployed_commit: Optional[str]
    last_update_ts: datetime.datetime

    @classmethod
    def from_orm(cls, orm: PreviewBranchStateORM) -> "PreviewBranchState":
        return cls(
            branch_name=orm.branch_name,
            is_active=orm.is_active,
            deployed_commit=orm.deployed_commit,
            last_update_ts=orm.last_update_ts,
        )
