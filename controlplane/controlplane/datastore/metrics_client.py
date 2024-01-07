import datetime
from typing import List, cast, Sequence, Optional, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controlplane.datastore.types.vmmetrics.cpu import (
    CpuVmMetricORM,
    CpuVmMetric,
    CpuVmMetricLatestORM,
    CpuVmMetricLatest,
)


from controlplane.datastore.types.utils import gen_random_uuid
from controlplane.datastore.config import DatastoreConfig
from sqlalchemy.dialects.postgresql import insert


def get_metric_id(vm_id: str, ts: datetime.datetime) -> str:
    epoch_millis = int(ts.timestamp() * 1000)
    return f"{vm_id}-{epoch_millis}-{gen_random_uuid()}"


class DatastoreMetricsClient:
    def __init__(self, config: DatastoreConfig):
        self.config = config
        url = config.get_url()
        self.engine = create_engine(url, echo=self.config.verbose_orm)

    def add_cpu_measurement(
        self, vm_id: str, cpu_percents: Sequence[float], ts: datetime.datetime
    ) -> None:
        """Add a CPU measurement for a VM. Updates both the timeseries table and the point-in-time table"""
        metric = CpuVmMetricORM(
            metric_id=get_metric_id(vm_id, ts),
            vm_id=vm_id,
            ts=ts,
            cpu_percents=cpu_percents,
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
                )
                .on_conflict_do_update(
                    index_elements=["vm_id"],
                    set_=dict(
                        ts=ts,
                        cpu_percents=cpu_percents,
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

    # Generic method for adding measurements
    def add_measurement(
        self,
        vm_id: str,
        ts: datetime.datetime,
        metrics: Sequence[float],  # TODO: Replace this
        metric_orm,
        latest_metric_orm,
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
    def get_measurements(
        self,
        vm_ids: List[str],
        metric_orm,
        metric_from_orm,
        start_ts: Optional[datetime.datetime] = None,
        end_ts: Optional[datetime.datetime] = None,
    ) -> List[Any]:
        results = []
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
                result_metric = metric_from_orm(row)
                results.append(result_metric)
        return results

    # Generic method for getting latest measurements
    def get_latest_measurements(
        self, vm_ids: List[str], latest_metric_orm, metric_from_orm
    ) -> List[Any]:
        if len(vm_ids) == 0:
            return []
        results = []

        with Session(bind=self.engine) as session:
            rows = (
                session.query(latest_metric_orm)
                .filter(latest_metric_orm.vm_id.in_(vm_ids))
                .all()
            )
            for row in rows:
                row = cast(latest_metric_orm, row)  # type: ignore
                result_metric = metric_from_orm(row)
                results.append(result_metric)
        return results

    # Generic method for deleting old measurements
    def delete_old_measurements(
        self,
        oldest_ts_to_keep: datetime.datetime,
        metric_orm,
        vm_ids: Optional[list[str]] = None,
    ) -> None:
        filters = [metric_orm.ts < oldest_ts_to_keep]
        if vm_ids is not None:
            filters.append(metric_orm.vm_id.in_(vm_ids))
        with Session(bind=self.engine) as session:
            session.query(metric_orm).filter(*filters).delete()
            session.commit()

    # ... specific metric methods (e.g., add_cpu_measurement) calling the generic methods ...
