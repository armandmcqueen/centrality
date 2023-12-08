from controlplane.datastore.types.base import DatastoreBase
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped,mapped_column
from dataclasses import dataclass
import uuid


def gen_random_uuid():
    """ Generate a random UUID as a string"""
    return str(uuid.uuid4())


def gen_random_token():
    """ Generate a random UUID as a string"""
    return f"centrality-{uuid.uuid4()}"

class UserTokenORM(DatastoreBase):
    __tablename__ = "user_account"

    user_id: Mapped[str] = mapped_column(primary_key=True, default=gen_random_uuid)
    token: Mapped[str] = mapped_column(nullable=False, unique=True, default=gen_random_token)


@dataclass
class UserToken:
    user_id: str
    token: str

    def __str__(self):
        return f"UserToken(user_id={self.user_id}, token={self.token})"

    @classmethod
    def from_orm(cls, orm: UserTokenORM) -> "UserToken":
        return cls(orm.user_id, orm.token)


