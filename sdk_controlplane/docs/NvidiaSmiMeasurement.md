# NvidiaSmiMeasurement

A measurement of NvidiaSmi

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vm_id** | **str** |  | 
**ts** | **datetime** |  | 
**nvidia_smi_output** | **str** |  | 

## Example

```python
from centrality_controlplane_sdk.models.nvidia_smi_measurement import NvidiaSmiMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of NvidiaSmiMeasurement from a JSON string
nvidia_smi_measurement_instance = NvidiaSmiMeasurement.from_json(json)
# print the JSON string representation of the object
print NvidiaSmiMeasurement.to_json()

# convert the object into a dict
nvidia_smi_measurement_dict = nvidia_smi_measurement_instance.to_dict()
# create an instance of NvidiaSmiMeasurement from a dict
nvidia_smi_measurement_form_dict = nvidia_smi_measurement.from_dict(nvidia_smi_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


