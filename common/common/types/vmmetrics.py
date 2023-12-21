import datetime
from typing import List
from pydantic import BaseModel


class CpuMeasurement(BaseModel):
    """A single CPU measurement, with a list of CPU percents for each core"""

    vm_id: str
    ts: datetime.datetime
    cpu_percents: List[float]

    @property
    def avg_cpu_percent(self) -> float:
        return sum(self.cpu_percents) / len(self.cpu_percents)
