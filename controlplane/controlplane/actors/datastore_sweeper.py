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

    sweep_interval_secs: int = 60 * 60 * 12  # 12 hours
    data_retention_secs: int = 60 * 60 * 24 * 7  # 7 days
    reap_vms_interval_secs: int = (
        15  # How often to check for dead vms that need to be reaped
    )
    vm_no_heartbeat_reap_secs: int = (
        constants.VM_NO_HEARTBEAT_DEATH_SECS
    )  # Allow this value to be overridden for testing


class SweepDatastore(conclib.ActorMessage):
    """Tell the DatastoreSweeper to prune old metric data"""

    pass


class ReapDisconnectedVms(conclib.ActorMessage):
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
        # ReapDisconnectedVms interval is set in __init__ below
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
        self.TICKS[ReapDisconnectedVms] = self.sweeper_config.reap_vms_interval_secs
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
                self.datastore_client.delete_old_cpu_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
            except Exception as e:
                # TODO: Eventually send an alert/event
                print(f"🚨 DatastoreSweeper - failed to sweep the datastore: {e}")
        elif isinstance(message, ReapDisconnectedVms):
            try:
                delta = timedelta(seconds=self.sweeper_config.vm_no_heartbeat_reap_secs)
                self.datastore_client.remove_vms_without_recent_healthcheck(
                    oldest_ts_to_keep=now - delta
                )
            except Exception as e:
                # TODO: Eventually send an alert/event
                print(f"🚨 DatastoreSweeper - failed to reap dead vms: {e}")

        else:
            raise conclib.errors.UnexpectedMessageError(message)
