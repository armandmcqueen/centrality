# DiskThroughput


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**disk_name** | **str** |  | 
**read_mbps** | **float** |  | 
**write_mbps** | **float** |  | 

## Example

```python
from centrality_controlplane_sdk.models.disk_throughput import DiskThroughput

# TODO update the JSON string below
json = "{}"
# create an instance of DiskThroughput from a JSON string
disk_throughput_instance = DiskThroughput.from_json(json)
# print the JSON string representation of the object
print DiskThroughput.to_json()

# convert the object into a dict
disk_throughput_dict = disk_throughput_instance.to_dict()
# create an instance of DiskThroughput from a dict
disk_throughput_form_dict = disk_throughput.from_dict(disk_throughput_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


