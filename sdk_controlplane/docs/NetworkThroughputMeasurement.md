# NetworkThroughputMeasurement

A measurement of NetworkThroughput

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vm_id** | **str** |  | 
**ts** | **datetime** |  | 
**per_interface** | [**Dict[str, Throughput]**](Throughput.md) |  | 
**total** | [**Throughput**](Throughput.md) |  | 

## Example

```python
from centrality_controlplane_sdk.models.network_throughput_measurement import NetworkThroughputMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of NetworkThroughputMeasurement from a JSON string
network_throughput_measurement_instance = NetworkThroughputMeasurement.from_json(json)
# print the JSON string representation of the object
print NetworkThroughputMeasurement.to_json()

# convert the object into a dict
network_throughput_measurement_dict = network_throughput_measurement_instance.to_dict()
# create an instance of NetworkThroughputMeasurement from a dict
network_throughput_measurement_form_dict = network_throughput_measurement.from_dict(network_throughput_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


