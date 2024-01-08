PerDiskIops = dict[str, float]

metric_obj_fields = """\
    iops: PerDiskIops
"""
metric_name_lowercase = "disk_iops"
metric_name_camelcase = "DiskIops"
metrics_shape_db = "dict[str, float]"
example_metrics = "{disk1: iopsXXX, disk2: iopsYYY}"
custom_types = """\
PerDiskIops = dict[str, float]
"""


def convert(metrics: PerDiskIops) -> dict[str, PerDiskIops]:
    return dict(iops=metrics)
