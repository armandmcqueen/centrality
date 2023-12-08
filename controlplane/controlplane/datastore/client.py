from typing import List, cast, Sequence

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controlplane.datastore.types.base import DatastoreBase
from controlplane.datastore.types.auth import UserTokenORM, UserToken
from controlplane.datastore.config import DatastoreConfig


class DatastoreClient:
    def __init__(self, config: DatastoreConfig):
        self.config = config
        self.engine = create_engine(config.get_url(), echo=self.config.verbose_orm)

        DatastoreBase.metadata.create_all(self.engine)

    def new_token(self) -> UserToken:
        """ Create a new token and add it to the database"""
        user_token = UserTokenORM()
        with Session(bind=self.engine) as session:
            session.add(user_token)
            session.commit()
            return UserToken.from_orm(user_token)

    def _add_dev_token(self) -> None:
        """ Add the dev token to the database"""
        user_token = UserTokenORM(user_id="dev", token="dev")
        with Session(bind=self.engine) as session:
            session.add(user_token)
            session.commit()


    def get_tokens(self) -> List[UserToken]:
        """ Get all tokens from the database"""
        results = []
        with Session(bind=self.engine) as session:
            rows = session.query(UserTokenORM).all()
            for row in rows:
                row = cast(UserTokenORM, row)
                result_token = UserToken.from_orm(row)
                results.append(result_token)
        return results

    def validate_token(self, user_id: str, token: str) -> bool:
        """ Check if a token is valid"""
        with Session(bind=self.engine) as session:
            row = session.query(UserTokenORM).filter(UserTokenORM.user_id == user_id).first()
            if row is None:
                return False
            row = cast(UserTokenORM, row)
            result_token = UserToken.from_orm(row)
            return result_token.token == token

    def reset_db(self):
        """ Drop all tables and recreate them"""
        DatastoreBase.metadata.drop_all(self.engine)
        DatastoreBase.metadata.create_all(self.engine)
        self._add_dev_token()
