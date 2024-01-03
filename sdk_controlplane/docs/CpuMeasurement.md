# CpuMeasurement

A single CPU measurement, with a list of CPU percents for each core

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vm_id** | **str** |  | 
**ts** | **datetime** |  | 
**cpu_percents** | **List[float]** |  | 

## Example

```python
from centrality_controlplane_sdk.models.cpu_measurement import CpuMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of CpuMeasurement from a JSON string
cpu_measurement_instance = CpuMeasurement.from_json(json)
# print the JSON string representation of the object
print CpuMeasurement.to_json()

# convert the object into a dict
cpu_measurement_dict = cpu_measurement_instance.to_dict()
# create an instance of CpuMeasurement from a dict
cpu_measurement_form_dict = cpu_measurement.from_dict(cpu_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


