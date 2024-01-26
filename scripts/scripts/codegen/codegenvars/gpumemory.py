from pydantic import BaseModel
from typing import Any

metric_obj_fields = """\
    memory: list[GpuMemory] = Field(..., description="A list with GPU memory usage for each GPU. There will be one entry per GPU. The order of the GPUs is the same as in the output of nvidia-smi.")
"""
metric_name_lowercase = "gpu_memory"
metric_name_camelcase = "GpuMemory"
metric_name_capitalized = "GPU_MEMORY"
metrics_shape_db = "list[list[float]]"
metrics_type_db = "JSONB"
example_metrics = "[[used, total], [used, total]]"
custom_types = """\
class GpuMemory(BaseModel):
    used_mb: float = Field(..., description="The used GPU memory in MiB.")
    total_mb: float = Field(..., description="The total GPU memory in MiB.")
"""


class GpuMemory(BaseModel):
    used_mb: float
    total_mb: float


def convert_from_metrics(metrics: list[list[float]]) -> dict[str, list[GpuMemory]]:
    memory = [
        GpuMemory(used_mb=memory_vals[0], total_mb=memory_vals[1])
        for memory_vals in metrics
    ]

    return dict(memory=memory)


def convert_to_metrics(self: Any) -> list[list[float]]:
    return [[memory.used_mb, memory.total_mb] for memory in self.memory]
