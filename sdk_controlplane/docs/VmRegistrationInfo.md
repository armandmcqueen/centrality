# VmRegistrationInfo

Information about a VM to register with the control plane.  Same as VM heartbeat, but without a few fields that are either set via URL params or automatically set server-side.

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
from centrality_controlplane_sdk.models.vm_registration_info import VmRegistrationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of VmRegistrationInfo from a JSON string
vm_registration_info_instance = VmRegistrationInfo.from_json(json)
# print the JSON string representation of the object
print VmRegistrationInfo.to_json()

# convert the object into a dict
vm_registration_info_dict = vm_registration_info_instance.to_dict()
# create an instance of VmRegistrationInfo from a dict
vm_registration_info_form_dict = vm_registration_info.from_dict(vm_registration_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


