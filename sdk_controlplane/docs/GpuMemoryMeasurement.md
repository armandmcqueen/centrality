# GpuMemoryMeasurement

A measurement of GpuMemory

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vm_id** | **str** |  | 
**ts** | **datetime** |  | 
**memory** | [**List[GpuMemory]**](GpuMemory.md) |  | 

## Example

```python
from centrality_controlplane_sdk.models.gpu_memory_measurement import GpuMemoryMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of GpuMemoryMeasurement from a JSON string
gpu_memory_measurement_instance = GpuMemoryMeasurement.from_json(json)
# print the JSON string representation of the object
print GpuMemoryMeasurement.to_json()

# convert the object into a dict
gpu_memory_measurement_dict = gpu_memory_measurement_instance.to_dict()
# create an instance of GpuMemoryMeasurement from a dict
gpu_memory_measurement_form_dict = gpu_memory_measurement.from_dict(gpu_memory_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


