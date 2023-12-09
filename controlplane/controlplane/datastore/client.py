import datetime
from typing import List, cast, Sequence, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.auth import UserTokenORM, UserToken
from controlplane.datastore.types.vmmetrics import CpuVmMetricORM, CpuVmMetric
from controlplane.datastore.types.utils import gen_random_uuid
from controlplane.datastore.config import DatastoreConfig


class DatastoreClient:
    def __init__(self, config: DatastoreConfig):
        self.config = config
        self.engine = create_engine(config.get_url(), echo=self.config.verbose_orm)

        DatastoreBaseORM.metadata.create_all(self.engine)

    def reset_db(self):
        """Drop all tables and recreate them"""
        DatastoreBaseORM.metadata.drop_all(self.engine)
        DatastoreBaseORM.metadata.create_all(self.engine)
        self._add_dev_token()

    def new_token(self) -> UserToken:
        """Create a new token and add it to the database"""
        user_token = UserTokenORM()
        with Session(bind=self.engine) as session:
            session.add(user_token)
            session.commit()
            return UserToken.from_orm(user_token)

    def _add_dev_token(self) -> None:
        """Add the dev token to the database"""
        user_token = UserTokenORM(user_id="dev", token="dev")
        with Session(bind=self.engine) as session:
            session.add(user_token)
            session.commit()

    def get_tokens(self) -> List[UserToken]:
        """Get all tokens from the database"""
        results = []
        with Session(bind=self.engine) as session:
            rows = session.query(UserTokenORM).all()
            for row in rows:
                row = cast(UserTokenORM, row)
                result_token = UserToken.from_orm(row)
                results.append(result_token)
        return results

    def validate_token(self, user_id: str, token: str) -> bool:
        """Check if a token is valid"""
        with Session(bind=self.engine) as session:
            row = (
                session.query(UserTokenORM)
                .filter(UserTokenORM.user_id == user_id)
                .first()
            )
            if row is None:
                return False
            row = cast(UserTokenORM, row)
            result_token = UserToken.from_orm(row)
            return result_token.token == token

    def add_cpu_measurement(
        self, vm_id: str, cpu_percents: Sequence[float], ts: datetime.datetime
    ) -> None:
        avg_cpu_percent = sum(cpu_percents) / len(cpu_percents)
        epoch_millis = int(ts.timestamp() * 1000)
        metric_id = f"{vm_id}-{epoch_millis}-{gen_random_uuid()}"
        metric = CpuVmMetricORM(
            metric_id=metric_id,
            vm_id=vm_id,
            ts=ts,
            cpu_percents=cpu_percents,
            avg_cpu_percent=avg_cpu_percent,
        )
        with Session(bind=self.engine) as session:
            session.add(metric)
            session.commit()

    def get_cpu_measurements(
        self,
        vm_id: str,
        start_ts: Optional[datetime.datetime],
        end_ts: Optional[datetime.datetime],
    ) -> List[CpuVmMetric]:
        results = []
        with Session(bind=self.engine) as session:
            # Get rows with vm_id based on start_ts and end_ts
            # If the start_ts is None, get all rows with vm_id that are before end_ts
            # If the end_ts is None, get all rows with vm_id that are after start_ts
            # If both are None, get all rows with vm_id
            filter_args = [CpuVmMetricORM.vm_id == vm_id]
            if start_ts is not None:
                filter_args.append(CpuVmMetricORM.ts >= start_ts)
            if end_ts is not None:
                filter_args.append(CpuVmMetricORM.ts <= end_ts)

            rows = (
                session.query(CpuVmMetricORM)
                .filter(*filter_args)
                .order_by(CpuVmMetricORM.ts)
                .all()
            )
            for row in rows:
                row = cast(CpuVmMetricORM, row)
                result_metric = CpuVmMetric.from_orm(row)
                results.append(result_metric)
        return results
