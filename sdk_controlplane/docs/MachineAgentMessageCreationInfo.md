# MachineAgentMessageCreationInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_id** | **str** |  | 
**is_ask** | **bool** |  | 
**msg_type** | **str** |  | 
**msg_content** | **str** |  | 
**max_response_chars** | **int** |  | 

## Example

```python
from centrality_controlplane_sdk.models.machine_agent_message_creation_info import MachineAgentMessageCreationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MachineAgentMessageCreationInfo from a JSON string
machine_agent_message_creation_info_instance = MachineAgentMessageCreationInfo.from_json(json)
# print the JSON string representation of the object
print MachineAgentMessageCreationInfo.to_json()

# convert the object into a dict
machine_agent_message_creation_info_dict = machine_agent_message_creation_info_instance.to_dict()
# create an instance of MachineAgentMessageCreationInfo from a dict
machine_agent_message_creation_info_form_dict = machine_agent_message_creation_info.from_dict(machine_agent_message_creation_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


