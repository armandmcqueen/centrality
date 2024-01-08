from pydantic import BaseModel

metric_obj_fields = """\
    memory: list[GpuMemory]
"""
metric_name_lowercase = "gpu_memory"
metric_name_camelcase = "GpuMemory"
metrics_shape_db = "list[list[float]]"
example_metrics = "[[used, total], [used, total]]"
custom_types = """\
class GpuMemory(BaseModel):
    used_mb: float
    total_mb: float
"""


class GpuMemory(BaseModel):
    used_mb: float
    total_mb: float


def convert(metrics: list[list[float]]) -> dict[str, list[GpuMemory]]:
    memory = [
        GpuMemory(used_mb=memory_vals[0], total_mb=memory_vals[1])
        for memory_vals in metrics
    ]

    return dict(memory=memory)
