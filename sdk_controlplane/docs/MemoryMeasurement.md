# MemoryMeasurement

A measurement of Memory

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** | The machine_id of the machine that generated this measurement | 
**ts** | **datetime** | The timestamp of the measurement | 
**free_memory_mb** | **float** | The free memory in MiB. | 
**total_memory_mb** | **float** | The total memory in MiB. | 

## Example

```python
from centrality_controlplane_sdk.models.memory_measurement import MemoryMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryMeasurement from a JSON string
memory_measurement_instance = MemoryMeasurement.from_json(json)
# print the JSON string representation of the object
print MemoryMeasurement.to_json()

# convert the object into a dict
memory_measurement_dict = memory_measurement_instance.to_dict()
# create an instance of MemoryMeasurement from a dict
memory_measurement_form_dict = memory_measurement.from_dict(memory_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


