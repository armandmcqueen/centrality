# DiskIopsMeasurement

A measurement of DiskIops

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** |  | 
**ts** | **datetime** |  | 
**iops** | [**List[DiskIops]**](DiskIops.md) |  | 

## Example

```python
from centrality_controlplane_sdk.models.disk_iops_measurement import DiskIopsMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of DiskIopsMeasurement from a JSON string
disk_iops_measurement_instance = DiskIopsMeasurement.from_json(json)
# print the JSON string representation of the object
print DiskIopsMeasurement.to_json()

# convert the object into a dict
disk_iops_measurement_dict = disk_iops_measurement_instance.to_dict()
# create an instance of DiskIopsMeasurement from a dict
disk_iops_measurement_form_dict = disk_iops_measurement.from_dict(disk_iops_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


