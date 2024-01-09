# DiskIops


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**disk_name** | **str** |  | 
**iops** | **float** |  | 

## Example

```python
from centrality_controlplane_sdk.models.disk_iops import DiskIops

# TODO update the JSON string below
json = "{}"
# create an instance of DiskIops from a JSON string
disk_iops_instance = DiskIops.from_json(json)
# print the JSON string representation of the object
print DiskIops.to_json()

# convert the object into a dict
disk_iops_dict = disk_iops_instance.to_dict()
# create an instance of DiskIops from a dict
disk_iops_form_dict = disk_iops.from_dict(disk_iops_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


