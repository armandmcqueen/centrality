import datetime

import conclib

from common import constants
from controlplane.datastore.config import DatastoreConfig
from controlplane.datastore.client import DatastoreClient
from common.config.config import CentralityConfig


class DatastoreSweeperConfig(CentralityConfig):
    sweep_interval_secs: int = 60 * 60 * 12  # 12 hours
    retention_secs: int = 60 * 60 * 24 * 7  # 7 days


class SweepDatastore(conclib.ActorMessage):
    pass


class DatastoreSweeper(conclib.PeriodicActor):
    URN = constants.CONTROL_PLANE_DATASTORE_SWEEPER_ACTOR
    TICKS = {}

    def __init__(
        self,
        datastore_sweeper_config: DatastoreSweeperConfig,
        datastore_config: DatastoreConfig,
    ):
        self.datastore_sweeper_config = datastore_sweeper_config
        self.datastore_config = datastore_config
        self.datastore_client = DatastoreClient(config=self.datastore_config)
        self.TICKS = {
            SweepDatastore: self.datastore_sweeper_config.sweep_interval_secs,
        }
        super().__init__()

    def on_receive(self, message: conclib.ActorMessage) -> None:
        if isinstance(message, SweepDatastore):
            try:
                retention_timedelta = datetime.timedelta(
                    seconds=self.datastore_sweeper_config.retention_secs
                )
                oldest_ts = (
                    datetime.datetime.now(datetime.timezone.utc) - retention_timedelta
                )
                self.datastore_client.delete_old_cpu_measurements(
                    oldest_ts_to_keep=oldest_ts,
                )
            except Exception as e:
                # TODO: This is a problem - send an alert?
                print(f"🚨 DatastoreSweeper - failed to clean up datastore: {e}")
        else:
            raise conclib.errors.UnexpectedMessageError(message)
