from controlplane.datastore.types.base import DatastoreBaseORM
from controlplane.datastore.types.auth import UserTokenORM, UserToken
from controlplane.datastore.types.vmliveness import (
    VmInfoOrm,
    VmInfo,
    VmRegistrationInfo,
)
import datetime
from typing import (
    List,
    Any,
    Optional,
    TypeVar,
    cast,
)


from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from controlplane.datastore.types.vmmetrics.metric import (
    MetricBaseORM,
    MetricLatestBaseORM,
    MetricBaseModel,
    MetricLatestBaseModel,
)
from controlplane.datastore.types.vmmetrics.generated.cpu import (
    CpuMetricORM,
    CpuMetricLatestORM,
    CpuMetric,
    CpuMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.disk_iops import (
    DiskIopsMetricORM,
    DiskIopsMetricLatestORM,
    DiskIopsMetric,
    DiskIopsMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.disk_throughput import (
    DiskThroughputMetricORM,
    DiskThroughputMetricLatestORM,
    DiskThroughputMetric,
    DiskThroughputMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.disk_usage import (
    DiskUsageMetricORM,
    DiskUsageMetricLatestORM,
    DiskUsageMetric,
    DiskUsageMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.gpu_memory import (
    GpuMemoryMetricORM,
    GpuMemoryMetricLatestORM,
    GpuMemoryMetric,
    GpuMemoryMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.gpu_utilization import (
    GpuUtilizationMetricORM,
    GpuUtilizationMetricLatestORM,
    GpuUtilizationMetric,
    GpuUtilizationMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.memory import (
    MemoryMetricORM,
    MemoryMetricLatestORM,
    MemoryMetric,
    MemoryMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.network_throughput import (
    NetworkThroughputMetricORM,
    NetworkThroughputMetricLatestORM,
    NetworkThroughputMetric,
    NetworkThroughputMetricLatest,
)
from controlplane.datastore.types.vmmetrics.generated.nvidia_smi import (
    NvidiaSmiMetricORM,
    NvidiaSmiMetricLatestORM,
    NvidiaSmiMetric,
    NvidiaSmiMetricLatest,
)


from controlplane.datastore.types.utils import gen_random_uuid
from controlplane.datastore.config import DatastoreConfig
from sqlalchemy.dialects.postgresql import insert


def get_metric_id(vm_id: str, ts: datetime.datetime) -> str:
    epoch_millis = int(ts.timestamp() * 1000)
    return f"{vm_id}-{epoch_millis}-{gen_random_uuid()}"


TMetricBaseModel = TypeVar("TMetricBaseModel", bound=MetricBaseModel)
TMetricLatestBaseModel = TypeVar("TMetricLatestBaseModel", bound=MetricLatestBaseModel)


class VmRegistrationConflictError(Exception):
    """
    Raised when a VM tries to register with a different machine spec than what is
    already in the database
    """

    pass


class VmHeartbeatBeforeRegistrationError(Exception):
    """
    Raised when a VM tries to heartbeat before registering
    """

    pass


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

    def token_exists(self, token: str) -> bool:
        """Check if a token is valid"""
        with Session(bind=self.engine) as session:
            row = (
                session.query(UserTokenORM).filter(UserTokenORM.token == token).first()
            )
            if row is None:
                return False
            return True

    def add_or_update_vm_info(
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
            existing_vm = (
                session.query(VmInfoOrm).filter(VmInfoOrm.vm_id == vm_id).first()
            )
            # If the VM is not already registered, add it
            if existing_vm is None:
                registration = registration_info.to_vm_info_orm(vm_id=vm_id)
                session.add(registration)
                session.commit()

            # Otherwise, confirm that the registration info matches what is already in the database,
            # except for nvidia-driver-version, which is a software version that can change.
            else:
                skipped_fields = ["nvidia_driver_version"]
                existing_vm = cast(VmInfoOrm, existing_vm)
                previous_registration_info = VmInfo.from_orm(existing_vm)
                for field in VmRegistrationInfo.model_fields.keys():
                    if field in skipped_fields:
                        continue
                    if getattr(previous_registration_info, field) != getattr(
                        registration_info, field
                    ):
                        raise VmRegistrationConflictError(
                            f"VM registration info does not match what is already in the database. "
                            f"Field: {field}, existing: {getattr(existing_vm, field)}, "
                            f"new: {getattr(registration_info, field)}."
                        )

                # Update the registration timestamp and last heartbeat timestamp in the DB
                existing_vm.registration_ts = datetime.datetime.now(
                    datetime.timezone.utc
                )
                existing_vm.last_heartbeat_ts = datetime.datetime.now(
                    datetime.timezone.utc
                )
                session.commit()

    def update_vm_info_heartbeat_ts(
        self,
        vm_id: str,
    ) -> None:
        """Set the last heartbeat for a VM to be the current time"""
        with Session(bind=self.engine) as session:
            existing_vm = (
                session.query(VmInfoOrm).filter(VmInfoOrm.vm_id == vm_id).first()
            )
            if existing_vm is None:
                raise VmHeartbeatBeforeRegistrationError(
                    f"VM {vm_id} is reporting heartbeat, but has not registered yet"
                )
            existing_vm = cast(VmInfoOrm, existing_vm)
            existing_vm.last_heartbeat_ts = datetime.datetime.utcnow()
            session.commit()

    def delete_vm_info(
        self,
        vm_id: str,
    ) -> None:
        """Remove the VM from the list of active VMs."""
        with Session(bind=self.engine) as session:
            delete_stmt = delete(VmInfoOrm).where(VmInfoOrm.vm_id == vm_id)
            session.execute(delete_stmt)
            session.commit()

    def remove_vms_without_recent_healthcheck(
        self,
        oldest_ts_to_keep: datetime.datetime,
    ) -> None:
        """Delete all VMs that have not reported a heartbeat since oldest_ts_to_keep"""
        with Session(bind=self.engine) as session:
            delete_stmt = delete(VmInfoOrm).where(
                VmInfoOrm.last_heartbeat_ts < oldest_ts_to_keep
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
                session.query(VmInfoOrm)
                .filter(VmInfoOrm.last_heartbeat_ts >= min_ts)
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
            rows = session.query(VmInfoOrm).all()
            return [row.vm_id for row in rows]

    ############################################################
    # Generic methods for adding, getting, and deleting metrics
    ############################################################

    # Generic method for adding measurements
    def _add_measurement(
        self,
        vm_id: str,
        ts: datetime.datetime,
        metrics: Any,
        metric_orm: type[MetricBaseORM],
        latest_metric_orm: type[MetricLatestBaseORM],
    ) -> None:
        metric = metric_orm(
            metric_id=get_metric_id(vm_id, ts),
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
        )
        with Session(bind=self.engine) as session:
            session.add(metric)

            # Upsert latest metric
            upsert_stmt = (
                insert(latest_metric_orm)
                .values(
                    vm_id=vm_id,
                    ts=ts,
                    metrics=metrics,
                )
                .on_conflict_do_update(
                    index_elements=["vm_id"],
                    set_=dict(
                        ts=ts,
                        metrics=metrics,
                    ),
                )
            )
            session.execute(upsert_stmt)
            session.commit()

    # Generic method for getting measurements
    def _get_measurements(
        self,
        metric_orm: type[MetricBaseORM],
        metric: type[TMetricBaseModel],
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[TMetricBaseModel]:
        results: list[TMetricBaseModel] = []
        with Session(bind=self.engine) as session:
            if len(vm_ids) == 0:
                return []
            filter_args: list[Any] = [metric_orm.vm_id.in_(vm_ids)]
            if start_ts is not None:
                filter_args.append(metric_orm.ts >= start_ts)
            if end_ts is not None:
                filter_args.append(metric_orm.ts <= end_ts)

            rows = (
                session.query(metric_orm)
                .filter(*filter_args)
                .order_by(metric_orm.ts)
                .all()
            )
            for row in rows:
                row = cast(metric_orm, row)  # type: ignore
                result_metric = metric.from_orm(orm=row)
                results.append(result_metric)
        return results

    # Generic method for getting latest measurements
    def _get_latest_measurements(
        self,
        vm_ids: list[str],
        latest_metric_orm: type[MetricLatestBaseORM],
        latest_metric: type[TMetricLatestBaseModel],
    ) -> list[TMetricLatestBaseModel]:
        if len(vm_ids) == 0:
            return []
        results: list[TMetricLatestBaseModel] = []

        with Session(bind=self.engine) as session:
            rows = (
                session.query(latest_metric_orm)
                .filter(latest_metric_orm.vm_id.in_(vm_ids))
                .all()
            )
            for row in rows:
                row = cast(latest_metric_orm, row)  # type: ignore
                result_metric = latest_metric.from_orm(orm=row)
                results.append(result_metric)
        return results

    # Generic method for deleting old measurements
    def _delete_old_measurements(
        self,
        metric_orm: type[MetricBaseORM],
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        filters = [metric_orm.ts < oldest_ts_to_keep]
        if vm_ids is not None:
            filters.append(metric_orm.vm_id.in_(vm_ids))
        with Session(bind=self.engine) as session:
            session.query(metric_orm).filter(*filters).delete()
            session.commit()

    ############################################################
    # Autogenerated code
    ############################################################
    # BEGIN GENERATED CODE

    # Cpu
    def add_cpu_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: list[float]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=CpuMetricORM,
            latest_metric_orm=CpuMetricLatestORM,
        )

    def get_cpu_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[CpuMetric]:
        return self._get_measurements(
            metric_orm=CpuMetricORM,
            metric=CpuMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_cpu_measurements(self, vm_ids: list[str]) -> list[CpuMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=CpuMetricLatestORM,
            latest_metric=CpuMetricLatest,
        )

    def delete_old_cpu_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=CpuMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # DiskIops
    def add_disk_iops_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: dict[str, float]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=DiskIopsMetricORM,
            latest_metric_orm=DiskIopsMetricLatestORM,
        )

    def get_disk_iops_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[DiskIopsMetric]:
        return self._get_measurements(
            metric_orm=DiskIopsMetricORM,
            metric=DiskIopsMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_disk_iops_measurements(
        self, vm_ids: list[str]
    ) -> list[DiskIopsMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=DiskIopsMetricLatestORM,
            latest_metric=DiskIopsMetricLatest,
        )

    def delete_old_disk_iops_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=DiskIopsMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # DiskUsage
    def add_disk_usage_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: dict[str, list[float]]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=DiskUsageMetricORM,
            latest_metric_orm=DiskUsageMetricLatestORM,
        )

    def get_disk_usage_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[DiskUsageMetric]:
        return self._get_measurements(
            metric_orm=DiskUsageMetricORM,
            metric=DiskUsageMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_disk_usage_measurements(
        self, vm_ids: list[str]
    ) -> list[DiskUsageMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=DiskUsageMetricLatestORM,
            latest_metric=DiskUsageMetricLatest,
        )

    def delete_old_disk_usage_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=DiskUsageMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # DiskThroughput
    def add_disk_throughput_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: dict[str, list[float]]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=DiskThroughputMetricORM,
            latest_metric_orm=DiskThroughputMetricLatestORM,
        )

    def get_disk_throughput_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[DiskThroughputMetric]:
        return self._get_measurements(
            metric_orm=DiskThroughputMetricORM,
            metric=DiskThroughputMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_disk_throughput_measurements(
        self, vm_ids: list[str]
    ) -> list[DiskThroughputMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=DiskThroughputMetricLatestORM,
            latest_metric=DiskThroughputMetricLatest,
        )

    def delete_old_disk_throughput_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=DiskThroughputMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # GpuMemory
    def add_gpu_memory_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: list[list[float]]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=GpuMemoryMetricORM,
            latest_metric_orm=GpuMemoryMetricLatestORM,
        )

    def get_gpu_memory_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[GpuMemoryMetric]:
        return self._get_measurements(
            metric_orm=GpuMemoryMetricORM,
            metric=GpuMemoryMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_gpu_memory_measurements(
        self, vm_ids: list[str]
    ) -> list[GpuMemoryMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=GpuMemoryMetricLatestORM,
            latest_metric=GpuMemoryMetricLatest,
        )

    def delete_old_gpu_memory_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=GpuMemoryMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # GpuUtilization
    def add_gpu_utilization_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: list[float]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=GpuUtilizationMetricORM,
            latest_metric_orm=GpuUtilizationMetricLatestORM,
        )

    def get_gpu_utilization_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[GpuUtilizationMetric]:
        return self._get_measurements(
            metric_orm=GpuUtilizationMetricORM,
            metric=GpuUtilizationMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_gpu_utilization_measurements(
        self, vm_ids: list[str]
    ) -> list[GpuUtilizationMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=GpuUtilizationMetricLatestORM,
            latest_metric=GpuUtilizationMetricLatest,
        )

    def delete_old_gpu_utilization_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=GpuUtilizationMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # Memory
    def add_memory_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: list[float]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=MemoryMetricORM,
            latest_metric_orm=MemoryMetricLatestORM,
        )

    def get_memory_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[MemoryMetric]:
        return self._get_measurements(
            metric_orm=MemoryMetricORM,
            metric=MemoryMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_memory_measurements(
        self, vm_ids: list[str]
    ) -> list[MemoryMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=MemoryMetricLatestORM,
            latest_metric=MemoryMetricLatest,
        )

    def delete_old_memory_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=MemoryMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # NetworkThroughput
    def add_network_throughput_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: dict[str, list[float]]
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=NetworkThroughputMetricORM,
            latest_metric_orm=NetworkThroughputMetricLatestORM,
        )

    def get_network_throughput_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[NetworkThroughputMetric]:
        return self._get_measurements(
            metric_orm=NetworkThroughputMetricORM,
            metric=NetworkThroughputMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_network_throughput_measurements(
        self, vm_ids: list[str]
    ) -> list[NetworkThroughputMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=NetworkThroughputMetricLatestORM,
            latest_metric=NetworkThroughputMetricLatest,
        )

    def delete_old_network_throughput_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=NetworkThroughputMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # NvidiaSmi
    def add_nvidia_smi_measurement(
        self, vm_id: str, ts: datetime.datetime, metrics: str
    ) -> None:
        self._add_measurement(
            vm_id=vm_id,
            ts=ts,
            metrics=metrics,
            metric_orm=NvidiaSmiMetricORM,
            latest_metric_orm=NvidiaSmiMetricLatestORM,
        )

    def get_nvidia_smi_measurements(
        self,
        vm_ids: list[str],
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> list[NvidiaSmiMetric]:
        return self._get_measurements(
            metric_orm=NvidiaSmiMetricORM,
            metric=NvidiaSmiMetric,
            vm_ids=vm_ids,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    def get_latest_nvidia_smi_measurements(
        self, vm_ids: list[str]
    ) -> list[NvidiaSmiMetricLatest]:
        return self._get_latest_measurements(
            vm_ids=vm_ids,
            latest_metric_orm=NvidiaSmiMetricLatestORM,
            latest_metric=NvidiaSmiMetricLatest,
        )

    def delete_old_nvidia_smi_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        self._delete_old_measurements(
            metric_orm=NvidiaSmiMetricORM,
            oldest_ts_to_keep=oldest_ts_to_keep,
            vm_ids=vm_ids,
        )

    # END GENERATED CODE
