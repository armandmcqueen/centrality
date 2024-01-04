import datetime
from typing import List, cast, Sequence, Optional, Any

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.auth import UserTokenORM, UserToken
from controlplane.datastore.types.vmmetrics import (
    CpuVmMetricORM,
    CpuVmMetric,
    CpuVmMetricLatestORM,
    CpuVmMetricLatest,
)
from controlplane.datastore.types.vmliveness import (
    VmHeartbeatORM,
    VmHeartbeat,
    VmRegistrationInfo,
)
from controlplane.datastore.types.utils import gen_random_uuid
from controlplane.datastore.config import DatastoreConfig
from sqlalchemy.dialects.postgresql import insert


class DatastoreClient:
    def __init__(self, config: DatastoreConfig):
        self.config = config
        url = config.get_url()
        self.engine = create_engine(url, echo=self.config.verbose_orm)

    def setup_db(self) -> None:
        """Create all tables if they don't exist"""
        DatastoreBaseORM.metadata.create_all(self.engine)
        self._add_dev_token()

    def reset_db(self) -> None:
        """Drop all tables and recreate them"""
        DatastoreBaseORM.metadata.drop_all(self.engine)
        self.setup_db()

    def new_token(self) -> UserToken:
        """Create a new token and add it to the database"""
        user_token = UserTokenORM()
        with Session(bind=self.engine) as session:
            session.add(user_token)
            session.commit()
            return UserToken.from_orm(user_token)

    def _add_dev_token(self) -> None:
        """Add the dev token to the database"""
        with Session(bind=self.engine) as session:
            upsert_stmt = (
                insert(UserTokenORM)
                .values(
                    user_id="dev",
                    token="dev",
                )
                .on_conflict_do_update(
                    index_elements=["user_id"], set_=dict(token="dev")
                )
            )
            session.execute(upsert_stmt)
            session.commit()

    def get_tokens(self) -> List[UserToken]:
        """Get all tokens from the database"""
        results = []
        with Session(bind=self.engine) as session:
            rows = session.query(UserTokenORM).all()
            for row in rows:
                row = cast(UserTokenORM, row)  # type: ignore
                result_token = UserToken.from_orm(orm=row)
                results.append(result_token)
        return results

    def validate_token(self, token: str) -> bool:
        # TODO: Rename this so it is clear that it returns a bool.
        #       Also rename this to be datastore oriented, not
        #       applicateion oriented
        """Check if a token is valid"""
        with Session(bind=self.engine) as session:
            row = (
                session.query(UserTokenORM).filter(UserTokenORM.token == token).first()
            )
            if row is None:
                return False
            return True

    def add_cpu_measurement(
        self, vm_id: str, cpu_percents: Sequence[float], ts: datetime.datetime
    ) -> None:
        """Add a CPU measurement for a VM. Updates both the timeseries table and the point-in-time table"""
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

            # Upsert latest metric
            upsert_stmt = (
                insert(CpuVmMetricLatestORM)
                .values(
                    vm_id=vm_id,
                    ts=ts,
                    cpu_percents=cpu_percents,
                    avg_cpu_percent=avg_cpu_percent,
                )
                .on_conflict_do_update(
                    index_elements=["vm_id"],
                    set_=dict(
                        ts=ts,
                        cpu_percents=cpu_percents,
                        avg_cpu_percent=avg_cpu_percent,
                    ),
                )
            )
            session.execute(upsert_stmt)
            session.commit()

    def get_cpu_measurements(
        self,
        vm_ids: List[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> List[CpuVmMetric]:
        results = []
        with Session(bind=self.engine) as session:
            if len(vm_ids) == 0:
                return []
            filter_args: list[Any] = [CpuVmMetricORM.vm_id.in_(vm_ids)]
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
                row = cast(CpuVmMetricORM, row)  # type: ignore
                result_metric = CpuVmMetric.from_orm(row)
                results.append(result_metric)
        return results

    def get_latest_cpu_measurements(
        self,
        vm_ids: List[str],
    ) -> List[CpuVmMetricLatest]:
        if len(vm_ids) == 0:
            return []
        results = []

        with Session(bind=self.engine) as session:
            rows = (
                session.query(CpuVmMetricLatestORM)
                .filter(CpuVmMetricLatestORM.vm_id.in_(vm_ids))
                .all()
            )
            for row in rows:
                row = cast(CpuVmMetricLatestORM, row)  # type: ignore
                result_metric = CpuVmMetricLatest.from_orm(row)
                results.append(result_metric)
        return results

    def delete_old_cpu_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        """Delete all CPU measurements older than oldest_ts_to_keep"""
        filters = [CpuVmMetricORM.ts < oldest_ts_to_keep]
        if vm_ids is not None:
            filters.append(CpuVmMetricORM.vm_id.in_(vm_ids))
        with Session(bind=self.engine) as session:
            session.query(CpuVmMetricORM).filter(*filters).delete()
            session.commit()

    def register_vm(  # TODO: Rename to be more datastore oriented instead of application oriented
        self,
        vm_id: str,
        registration_info: VmRegistrationInfo,
    ) -> None:
        """
        Register a VM with information about the machine.

        Will raise an exception if the VM is already registered with different machine specs. If the machine
        spec is the same, it will update the registration timestamp and last heartbeat timestamp.

        nvidia-driver-version is not checked for equality because it can be upgraded without changing
        VMs.
        """
        with Session(bind=self.engine) as session:
            # If the VM is not already registered, add it
            existing_vm = (
                session.query(VmHeartbeatORM)
                .filter(VmHeartbeatORM.vm_id == vm_id)
                .first()
            )
            if existing_vm is None:
                registration = registration_info.to_heartbeat_orm(vm_id=vm_id)
                session.add(registration)
                session.commit()
            else:
                # Otherwise, confirm that the registration info matches what is already in the database,
                # except for nvidia-driver-version
                skipped_fields = ["nvidia_driver_version"]
                existing_vm = cast(VmHeartbeatORM, existing_vm)
                previous_registration_info = VmHeartbeat.from_orm(existing_vm)
                for field in VmRegistrationInfo.model_fields.keys():
                    if field in skipped_fields:
                        continue
                    if getattr(previous_registration_info, field) != getattr(
                        registration_info, field
                    ):
                        # TODO: Use custom exception class and better error message that explains intended behavior to user
                        raise Exception(
                            f"VM registration info does not match what is already in the database. "
                            f"Field: {field}, existing: {getattr(existing_vm, field)}, "
                            f"new: {getattr(registration_info, field)}"
                        )

                # Update the registration timestamp and last heartbeat timestamp in the DB
                existing_vm.registration_ts = datetime.datetime.now(
                    datetime.timezone.utc
                )
                existing_vm.last_heartbeat_ts = datetime.datetime.now(
                    datetime.timezone.utc
                )
                session.commit()

    def report_heartbeat(  # TODO: Rename to be more datastore oriented instead of application oriented
        self,
        vm_id: str,
    ) -> None:
        """Set the last heartbeat for a VM to be the current time"""
        with Session(bind=self.engine) as session:
            existing_vm = (
                session.query(VmHeartbeatORM)
                .filter(VmHeartbeatORM.vm_id == vm_id)
                .first()
            )
            if existing_vm is None:
                # TODO: Improve this exception with custom class
                raise Exception(
                    f"VM {vm_id} is reporting heartbeat, but has not registered yet"
                )
            existing_vm = cast(VmHeartbeatORM, existing_vm)
            existing_vm.last_heartbeat_ts = datetime.datetime.utcnow()
            session.commit()

    def report_vm_death(
        self,
        vm_id: str,
    ) -> None:
        """Remove the VM from the list of active VMs."""
        with Session(bind=self.engine) as session:
            delete_stmt = delete(VmHeartbeatORM).where(VmHeartbeatORM.vm_id == vm_id)
            session.execute(delete_stmt)
            session.commit()

    def remove_vms_without_recent_healthcheck(
        self,
        oldest_ts_to_keep: datetime.datetime,
    ) -> None:
        """Delete all VMs that have not reported a heartbeat since oldest_ts_to_keep"""
        with Session(bind=self.engine) as session:
            delete_stmt = delete(VmHeartbeatORM).where(
                VmHeartbeatORM.last_heartbeat_ts < oldest_ts_to_keep
            )
            session.execute(delete_stmt)
            session.commit()

    def get_live_vms(
        self,
        liveness_threshold_secs: int,
    ) -> list[str]:
        """
        Get a list of VMs that have sent a heartbeat in the last liveness_threshold_secs seconds
        """
        # TODO: Convert to return machine info
        min_ts = datetime.datetime.utcnow() - datetime.timedelta(
            seconds=liveness_threshold_secs
        )
        with Session(bind=self.engine) as session:
            rows = (
                session.query(VmHeartbeatORM)
                .filter(VmHeartbeatORM.last_heartbeat_ts >= min_ts)
                .all()
            )
            return [row.vm_id for row in rows]

    def get_all_vms(
        self,
    ) -> list[str]:
        """
        Return the list of all VMs that are live or in limbo
        """
        with Session(bind=self.engine) as session:
            rows = session.query(VmHeartbeatORM).all()
            return [row.vm_id for row in rows]
