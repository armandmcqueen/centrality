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


class SweepDatastore(conclib.ActorMessage):
    """Tell the DatastoreSweeper to prune old data"""

    pass


class DatastoreSweeper(conclib.PeriodicActor):
    """
    Periodically prune old timeseries data from the datastore.
    """

    URN = constants.CONTROL_PLANE_DATASTORE_SWEEPER_ACTOR
    TICKS = {}  # Interval is set in __init__

    def __init__(
        self,
        datastore_sweeper_config: DatastoreSweeperConfig,
        datastore_config: DatastoreConfig,
    ):
        self.sweeper_config = datastore_sweeper_config
        self.datastore_config = datastore_config
        self.datastore_client = DatastoreClient(config=self.datastore_config)
        self.TICKS = {
            SweepDatastore: self.sweeper_config.sweep_interval_secs,
        }
        super().__init__()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SweepDatastore):
            try:
                now = datetime.now(timezone.utc)
                # print(f"🧹 DatastoreSweeper - current time is {now}")
                delta = timedelta(seconds=self.sweeper_config.data_retention_secs)
                # print(f"🧹 DatastoreSweeper - retention window is {delta}")
                oldest_ts = now - delta
                print(f"🧹 DatastoreSweeper - pruning data older than {oldest_ts}")
                self.datastore_client.delete_old_cpu_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
            except Exception as e:
                # TODO: Eventually send an alert/event
                print(f"🚨 DatastoreSweeper - failed to prune the datastore: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
