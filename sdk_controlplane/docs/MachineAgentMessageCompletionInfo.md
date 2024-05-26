# MachineAgentMessageCompletionInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**msg_id** | **str** |  | 
**errored** | **bool** |  | 
**outcome** | **str** |  | 

## Example

```python
from centrality_controlplane_sdk.models.machine_agent_message_completion_info import MachineAgentMessageCompletionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MachineAgentMessageCompletionInfo from a JSON string
machine_agent_message_completion_info_instance = MachineAgentMessageCompletionInfo.from_json(json)
# print the JSON string representation of the object
print MachineAgentMessageCompletionInfo.to_json()

# convert the object into a dict
machine_agent_message_completion_info_dict = machine_agent_message_completion_info_instance.to_dict()
# create an instance of MachineAgentMessageCompletionInfo from a dict
machine_agent_message_completion_info_form_dict = machine_agent_message_completion_info.from_dict(machine_agent_message_completion_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


