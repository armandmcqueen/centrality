CpuPercents = list[float]

metric_obj_fields = """\
    cpu_percents: CpuPercents
"""
metric_name_lowercase = "cpu"
metric_name_camelcase = "Cpu"
metrics_shape_db = "list[float]"
example_metrics = "[cpuWWW, cpuXXX, cpuYYY, cpuZZZ]"
custom_types = "CpuPercents = list[float]"


def convert(metrics: list[float]) -> dict[str, CpuPercents]:
    return dict(cpu_percents=metrics)
