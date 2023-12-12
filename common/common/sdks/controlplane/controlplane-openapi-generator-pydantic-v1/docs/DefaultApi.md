# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_auth_healthcheck_healthz_auth_get**](DefaultApi.md#get_auth_healthcheck_healthz_auth_get) | **GET** /healthz/auth | Get Auth Healthcheck
[**get_cpu_metric_metrics_cpu_get**](DefaultApi.md#get_cpu_metric_metrics_cpu_get) | **GET** /metrics/cpu | Get Cpu Metric
[**get_healthcheck_healthz_get**](DefaultApi.md#get_healthcheck_healthz_get) | **GET** /healthz | Get Healthcheck
[**put_cpu_metric_metrics_cpu_post**](DefaultApi.md#put_cpu_metric_metrics_cpu_post) | **POST** /metrics/cpu | Put Cpu Metric


# **get_auth_healthcheck_healthz_auth_get**
> OkResponse get_auth_healthcheck_healthz_auth_get()

Get Auth Healthcheck

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import openapi_client
from openapi_client.models.ok_response import OkResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Get Auth Healthcheck
        api_response = api_instance.get_auth_healthcheck_healthz_auth_get()
        print("The response of DefaultApi->get_auth_healthcheck_healthz_auth_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_auth_healthcheck_healthz_auth_get: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**OkResponse**](OkResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cpu_metric_metrics_cpu_get**
> List[CpuMeasurement] get_cpu_metric_metrics_cpu_get(vm_ids, from_ts=from_ts, to_ts=to_ts)

Get Cpu Metric

Get cpu metrics for certain VMs between from_ts to to_ts, inclusive. :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of CpuMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import openapi_client
from openapi_client.models.cpu_measurement import CpuMeasurement
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    vm_ids = ['vm_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Cpu Metric
        api_response = api_instance.get_cpu_metric_metrics_cpu_get(vm_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DefaultApi->get_cpu_metric_metrics_cpu_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_cpu_metric_metrics_cpu_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vm_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[CpuMeasurement]**](CpuMeasurement.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_healthcheck_healthz_get**
> get_healthcheck_healthz_get()

Get Healthcheck

### Example

```python
import time
import os
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Get Healthcheck
        api_instance.get_healthcheck_healthz_get()
    except Exception as e:
        print("Exception when calling DefaultApi->get_healthcheck_healthz_get: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_cpu_metric_metrics_cpu_post**
> OkResponse put_cpu_metric_metrics_cpu_post(cpu_measurement)

Put Cpu Metric

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import openapi_client
from openapi_client.models.cpu_measurement import CpuMeasurement
from openapi_client.models.ok_response import OkResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cpu_measurement = openapi_client.CpuMeasurement() # CpuMeasurement | 

    try:
        # Put Cpu Metric
        api_response = api_instance.put_cpu_metric_metrics_cpu_post(cpu_measurement)
        print("The response of DefaultApi->put_cpu_metric_metrics_cpu_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->put_cpu_metric_metrics_cpu_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cpu_measurement** | [**CpuMeasurement**](CpuMeasurement.md)|  | 

### Return type

[**OkResponse**](OkResponse.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

