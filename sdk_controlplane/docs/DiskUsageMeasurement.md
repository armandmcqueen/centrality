# DiskUsageMeasurement

A measurement of DiskUsage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** | The machine_id of the machine that generated this measurement | 
**ts** | **datetime** | The timestamp of the measurement | 
**usage** | [**Dict[str, DiskUsage]**](DiskUsage.md) | A dict with disk usage for each disk with the disk name as the key. | 

## Example

```python
from centrality_controlplane_sdk.models.disk_usage_measurement import DiskUsageMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of DiskUsageMeasurement from a JSON string
disk_usage_measurement_instance = DiskUsageMeasurement.from_json(json)
# print the JSON string representation of the object
print DiskUsageMeasurement.to_json()

# convert the object into a dict
disk_usage_measurement_dict = disk_usage_measurement_instance.to_dict()
# create an instance of DiskUsageMeasurement from a dict
disk_usage_measurement_form_dict = disk_usage_measurement.from_dict(disk_usage_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


