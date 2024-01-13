from rapidui.library.flexbox import CardContents, BaseCard
import datetime
from typing import Optional
import pandas as pd
import humanize


class MachineInfoCardContents(CardContents):
    machine_id: str
    last_heartbeat_ts_dt: datetime.datetime
    registration_ts_dt: datetime.datetime
    num_cpus: int
    cpu_description: str
    host_memory_mb: float
    num_gpus: int
    gpu_type: Optional[str]
    gpu_memory_mb: Optional[float]
    nvidia_driver_version: Optional[str]
    hostname: str

    @property
    def last_heartbeat_ts(self):
        return self.last_heartbeat_ts_dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    @property
    def registration_ts(self):
        return self.registration_ts_dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    def as_df(self):
        memory_human = humanize.naturalsize(
            self.host_memory_mb * 1024 * 1024, binary=True
        )
        df = pd.DataFrame.from_dict(
            {
                "Machine ID": [self.machine_id],
                "Hostname": [self.hostname],
                "Last Heartbeat": [self.last_heartbeat_ts],
                "Registration": [self.registration_ts],
                "CPUs": [self.num_cpus],
                "CPU Description": [self.cpu_description],
                "Host Memory": [memory_human],
                "GPUs": [self.num_gpus],
            }
        )
        if self.num_gpus > 0:
            gpu_memory_human = humanize.naturalsize(
                self.gpu_memory_mb * 1024 * 1024, binary=True
            )
            df["GPU Type"] = self.gpu_type
            df["GPU Memory"] = gpu_memory_human
            df["Nvidia Driver Version"] = self.nvidia_driver_version
        return df.transpose().astype(str)


class MachineInfoCard(BaseCard):
    def __init__(self, parent_container, contents: MachineInfoCardContents):
        self.container = parent_container
        self.contents = contents

        # save all the fields as a table
        self.table = self.container.empty()
        self._set_fields()

    def _set_fields(self):
        self.table.table(data=self.contents.as_df())

    def empty(self):
        self.table.empty()
        self.container.empty()

    def update(self, contents: MachineInfoCardContents):
        self.contents = contents
        self._set_fields()
