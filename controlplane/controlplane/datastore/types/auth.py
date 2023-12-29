from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.utils import gen_random_uuid
from pydantic import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
import uuid


def gen_random_token() -> str:
    """Generate a random UUID as a string"""
    return f"centrality-{uuid.uuid4()}"


class UserTokenORM(DatastoreBaseORM):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    token: Mapped[str] = mapped_column(
        nullable=False, unique=True, default=gen_random_token
    )


class UserToken(BaseModel):
    user_id: str
    token: str

    def __str__(self) -> str:
        return f"UserToken(user_id={self.user_id}, token={self.token})"

    @classmethod
    def from_orm(cls, orm: UserTokenORM) -> "UserToken":
        return cls(user_id=orm.user_id, token=orm.token)
