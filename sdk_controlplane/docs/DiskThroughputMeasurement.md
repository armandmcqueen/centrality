# DiskThroughputMeasurement

A measurement of DiskThroughput

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** | The machine_id of the machine that generated this measurement | 
**ts** | **datetime** | The timestamp of the measurement | 
**throughput** | [**List[DiskThroughput]**](DiskThroughput.md) |  | 

## Example

```python
from centrality_controlplane_sdk.models.disk_throughput_measurement import DiskThroughputMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of DiskThroughputMeasurement from a JSON string
disk_throughput_measurement_instance = DiskThroughputMeasurement.from_json(json)
# print the JSON string representation of the object
print DiskThroughputMeasurement.to_json()

# convert the object into a dict
disk_throughput_measurement_dict = disk_throughput_measurement_instance.to_dict()
# create an instance of DiskThroughputMeasurement from a dict
disk_throughput_measurement_form_dict = disk_throughput_measurement.from_dict(disk_throughput_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


