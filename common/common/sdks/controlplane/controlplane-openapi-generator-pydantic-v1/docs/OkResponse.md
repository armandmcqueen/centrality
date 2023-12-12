# OkResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] [default to 'ok']

## Example

```python
from openapi_client.models.ok_response import OkResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OkResponse from a JSON string
ok_response_instance = OkResponse.from_json(json)
# print the JSON string representation of the object
print OkResponse.to_json()

# convert the object into a dict
ok_response_dict = ok_response_instance.to_dict()
# create an instance of OkResponse from a dict
ok_response_form_dict = ok_response.from_dict(ok_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


