# MachineInfo

Information about a machine's current state

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** |  | 
**last_heartbeat_ts** | **datetime** |  | 
**registration_ts** | **datetime** |  | 
**num_cpus** | **int** |  | 
**cpu_description** | **str** |  | 
**host_memory_mb** | **int** |  | 
**num_gpus** | **int** |  | 
**gpu_type** | **str** |  | 
**gpu_memory_mb** | **int** |  | 
**nvidia_driver_version** | **str** |  | 
**hostname** | **str** |  | 

## Example

```python
from centrality_controlplane_sdk.models.machine_info import MachineInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MachineInfo from a JSON string
machine_info_instance = MachineInfo.from_json(json)
# print the JSON string representation of the object
print MachineInfo.to_json()

# convert the object into a dict
machine_info_dict = machine_info_instance.to_dict()
# create an instance of MachineInfo from a dict
machine_info_form_dict = machine_info.from_dict(machine_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


