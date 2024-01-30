# DiskUsage


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**disk_name** | **str** | The name of the disk, e.g. /dev/sda. | 
**used_mb** | **float** | The used disk space in MiB. | 
**total_mb** | **float** | The total space of the disk in MiB. | 

## Example

```python
from centrality_controlplane_sdk.models.disk_usage import DiskUsage

# TODO update the JSON string below
json = "{}"
# create an instance of DiskUsage from a JSON string
disk_usage_instance = DiskUsage.from_json(json)
# print the JSON string representation of the object
print DiskUsage.to_json()

# convert the object into a dict
disk_usage_dict = disk_usage_instance.to_dict()
# create an instance of DiskUsage from a dict
disk_usage_form_dict = disk_usage.from_dict(disk_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


