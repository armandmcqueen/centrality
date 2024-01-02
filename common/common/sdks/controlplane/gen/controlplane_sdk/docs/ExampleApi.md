# controlplane_sdk.ExampleApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**hello**](ExampleApi.md#hello) | **GET** /example/hello | Hello
[**hello_auth**](ExampleApi.md#hello_auth) | **GET** /example/hello/auth | Hello Auth


# **hello**
> hello()

Hello

### Example

```python
import time
import os
import controlplane_sdk
from controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = controlplane_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = controlplane_sdk.ExampleApi(api_client)

    try:
        # Hello
        api_instance.hello()
    except Exception as e:
        print("Exception when calling ExampleApi->hello: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **hello_auth**
> hello_auth()

Hello Auth

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import controlplane_sdk
from controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = controlplane_sdk.ExampleApi(api_client)

    try:
        # Hello Auth
        api_instance.hello_auth()
    except Exception as e:
        print("Exception when calling ExampleApi->hello_auth: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

