import datetime
from typing import List
from pydantic import BaseModel

# TODO: Remove this from common? The SDK will autogenerate the pydantic type based on the
#       OpenAPI spec, so we really don't need a common type system. Plus it introduced
#       bugs when I tried to add a property, which is not included in the gneeration.


class CpuMeasurement(BaseModel):
    """A single CPU measurement, with a list of CPU percents for each core"""

    machine_id: str
    ts: datetime.datetime
    cpu_percents: List[float]
