from datetime import timedelta, datetime, timezone

import conclib

from common import constants
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from common.config.config import CentralityConfig
from rich import print


class DatastoreSweeperConfig(CentralityConfig):
    """
    How often to sweep the datastore for old data, and how long to keep data points around.
    """

    sweep_interval_secs: int = 60 * 10  # 10 minutes
    data_retention_secs: int = 60 * 60 * 2  # 2 hours
    reap_machines_interval_secs: int = (
        15  # How often to check for dead machines that need to be reaped
    )
    machine_no_heartbeat_reap_secs: int = (
        constants.DEFAULT_MACHINE_NO_HEARTBEAT_DEATH_SECS
    )  # Allow this value to be overridden for testing


class SweepDatastore(conclib.ActorMessage):
    """Tell the DatastoreSweeper to prune old metric data"""

    pass


class ReapDisconnectedMachines(conclib.ActorMessage):
    """
    Tell the DatastoreSweeper to remove agents that haven't sent a heartbeat in a long time so
    they are officially dead, rather than in disconnect limbo
    """

    pass


class DatastoreSweeper(conclib.PeriodicActor):
    """
    Periodically prune old data from the datastore.
    """

    URN = constants.CONTROL_PLANE_DATASTORE_SWEEPER_ACTOR
    TICKS: dict[type[conclib.ActorMessage], int] = {
        # ReapDisconnectedMachines interval is set in __init__ below
        # SweepDatastore interval is set in __init__ below
    }

    def __init__(
        self,
        datastore_sweeper_config: DatastoreSweeperConfig,
        datastore_config: DatastoreConfig,
    ):
        self.sweeper_config = datastore_sweeper_config
        self.datastore_config = datastore_config
        self.datastore_client = DatastoreClient(config=self.datastore_config)
        self.TICKS[SweepDatastore] = self.sweeper_config.sweep_interval_secs
        self.TICKS[
            ReapDisconnectedMachines
        ] = self.sweeper_config.reap_machines_interval_secs
        super().__init__()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        now = datetime.now(timezone.utc)
        # print(f"🧹 DatastoreSweeper - current time is {now}")
        if isinstance(message, SweepDatastore):
            try:
                delta = timedelta(seconds=self.sweeper_config.data_retention_secs)
                # print(f"🧹 DatastoreSweeper - retention window is {delta}")
                oldest_ts = now - delta
                print(f"🧹 DatastoreSweeper - pruning data older than {oldest_ts}")
                # TODO: More granular logging and exception handling
                self.datastore_client.delete_old_cpu_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_disk_iops_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_disk_usage_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_disk_throughput_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_gpu_memory_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_gpu_utilization_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_memory_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
                self.datastore_client.delete_old_network_throughput_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
            except Exception as e:
                # TODO: Eventually send an alert/event
                print(f"🚨 DatastoreSweeper - failed to sweep the datastore: {e}")
        elif isinstance(message, ReapDisconnectedMachines):
            try:
                delta = timedelta(
                    seconds=self.sweeper_config.machine_no_heartbeat_reap_secs
                )
                self.datastore_client.remove_machines_without_recent_healthcheck(
                    oldest_ts_to_keep=now - delta
                )
            except Exception as e:
                # TODO: Eventually send an alert/event
                print(f"🚨 DatastoreSweeper - failed to reap dead machines: {e}")

        else:
            raise conclib.errors.UnexpectedMessageError(message)
