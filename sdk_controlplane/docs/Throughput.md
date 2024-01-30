# Throughput


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interface_name** | **str** | The name of the network interface, e.g. eth0. | 
**sent_mbps** | **float** | The sent throughput for the interface in MiB/s. | 
**recv_mbps** | **float** | The received throughput for the interface in MiB/s. | 

## Example

```python
from centrality_controlplane_sdk.models.throughput import Throughput

# TODO update the JSON string below
json = "{}"
# create an instance of Throughput from a JSON string
throughput_instance = Throughput.from_json(json)
# print the JSON string representation of the object
print Throughput.to_json()

# convert the object into a dict
throughput_dict = throughput_instance.to_dict()
# create an instance of Throughput from a dict
throughput_form_dict = throughput.from_dict(throughput_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


