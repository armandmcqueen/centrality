# GpuMemory


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**used_mb** | **float** |  | 
**total_mb** | **float** |  | 

## Example

```python
from centrality_controlplane_sdk.models.gpu_memory import GpuMemory

# TODO update the JSON string below
json = "{}"
# create an instance of GpuMemory from a JSON string
gpu_memory_instance = GpuMemory.from_json(json)
# print the JSON string representation of the object
print GpuMemory.to_json()

# convert the object into a dict
gpu_memory_dict = gpu_memory_instance.to_dict()
# create an instance of GpuMemory from a dict
gpu_memory_form_dict = gpu_memory.from_dict(gpu_memory_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


