import datetime
from typing import List, cast, Sequence, Optional

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.auth import UserTokenORM, UserToken
from controlplane.datastore.types.vmmetrics import CpuVmMetricORM, CpuVmMetric
from controlplane.datastore.types.vmliveness import VmHeartbeatORM, VmHeartbeat
from controlplane.datastore.types.utils import gen_random_uuid
from controlplane.datastore.config import DatastoreConfig
from sqlalchemy.dialects.postgresql import insert
import os


class DatastoreClient:
    def __init__(self, config: DatastoreConfig):
        self.config = config
        url = config.get_url()
        self.engine = create_engine(url, echo=self.config.verbose_orm)

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

    def validate_token(self, token: str) -> bool:
        """Check if a token is valid"""
        with Session(bind=self.engine) as session:
            row = (
                session.query(UserTokenORM)
                .filter(UserTokenORM.token == token)
                .first()
            )
            if row is None:
                return False
            return True

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
        vm_ids: List[str],
        start_ts: Optional[datetime.datetime],
        end_ts: Optional[datetime.datetime],
    ) -> List[CpuVmMetric]:
        results = []
        with Session(bind=self.engine) as session:
            if len(vm_ids) == 0:
                return []
            filter_args = [CpuVmMetricORM.vm_id.in_(vm_ids)]
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

    def get_latest_cpu_measurements(
        self,
        vm_ids: List[str],
    ) -> List[CpuVmMetric]:
        if len(vm_ids) == 0:
            return []
        results = []
        with Session(bind=self.engine) as session:
            filter_args = [CpuVmMetricORM.vm_id.in_(vm_ids)]

            # Get the most recent metric for each VM by filtering on the vm_id
            # and then getting the most recent timestamp
            subquery = (

                session.query(
                    CpuVmMetricORM.vm_id,
                    func.max(CpuVmMetricORM.ts).label('latest_ts')
                )
                .filter(*filter_args)
                .group_by(CpuVmMetricORM.vm_id)
                .subquery()
            )
            rows = (
                # This query gets the most recent metric for each vm_id
                session.query(CpuVmMetricORM)
                .join(subquery, CpuVmMetricORM.vm_id == subquery.c.vm_id)
                .filter(CpuVmMetricORM.ts == subquery.c.latest_ts)
                .all()
            )
            for row in rows:
                row = cast(CpuVmMetricORM, row)
                result_metric = CpuVmMetric.from_orm(row)
                results.append(result_metric)
        return results

    def report_heartbeat(
            self,
            vm_id: str,
    ):
        """ Set the last heartbeat for a VM to be the current time """
        with Session(bind=self.engine) as session:
            upsert_stmt = insert(VmHeartbeatORM).values(
                vm_id=vm_id,
                last_heartbeat_ts=datetime.datetime.utcnow()
            ).on_conflict_do_update(
                index_elements=['vm_id'],
                set_=dict(last_heartbeat_ts=datetime.datetime.utcnow())
            )
            session.execute(upsert_stmt)
            session.commit()

    def get_live_vms(
            self,
            liveness_threshold_secs: int,
    ) -> list[str]:
        """
        Get a list of VMs that have sent a heartbeat in the last liveness_threshold_secs seconds
        """
        min_ts = datetime.datetime.utcnow() - datetime.timedelta(seconds=liveness_threshold_secs)
        with Session(bind=self.engine) as session:
            rows = (
                session.query(VmHeartbeatORM)
                .filter(VmHeartbeatORM.last_heartbeat_ts >= min_ts)
                .all()
            )
            return [row.vm_id for row in rows]
