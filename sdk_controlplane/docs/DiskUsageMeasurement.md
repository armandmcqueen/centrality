# DiskUsageMeasurement

A measurement of DiskUsage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vm_id** | **str** |  | 
**ts** | **datetime** |  | 
**usage** | [**List[DiskUsage]**](DiskUsage.md) |  | 

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


