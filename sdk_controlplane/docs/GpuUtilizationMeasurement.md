# GpuUtilizationMeasurement

A measurement of GpuUtilization

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** |  | 
**ts** | **datetime** |  | 
**gpu_percents** | **List[float]** |  | 

## Example

```python
from centrality_controlplane_sdk.models.gpu_utilization_measurement import GpuUtilizationMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of GpuUtilizationMeasurement from a JSON string
gpu_utilization_measurement_instance = GpuUtilizationMeasurement.from_json(json)
# print the JSON string representation of the object
print GpuUtilizationMeasurement.to_json()

# convert the object into a dict
gpu_utilization_measurement_dict = gpu_utilization_measurement_instance.to_dict()
# create an instance of GpuUtilizationMeasurement from a dict
gpu_utilization_measurement_form_dict = gpu_utilization_measurement.from_dict(gpu_utilization_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


