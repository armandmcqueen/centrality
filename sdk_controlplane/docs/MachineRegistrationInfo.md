# MachineRegistrationInfo

Information about a machine to register with the control plane.  Same as machine heartbeat, but without a few fields that are either set via URL params or automatically set server-side.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
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
from centrality_controlplane_sdk.models.machine_registration_info import MachineRegistrationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MachineRegistrationInfo from a JSON string
machine_registration_info_instance = MachineRegistrationInfo.from_json(json)
# print the JSON string representation of the object
print MachineRegistrationInfo.to_json()

# convert the object into a dict
machine_registration_info_dict = machine_registration_info_instance.to_dict()
# create an instance of MachineRegistrationInfo from a dict
machine_registration_info_form_dict = machine_registration_info.from_dict(machine_registration_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


