# centrality_controlplane_sdk.DataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_auth_healthcheck**](DataApi.md#get_auth_healthcheck) | **GET** /healthz/auth | Get Auth Healthcheck
[**get_cpu_metrics**](DataApi.md#get_cpu_metrics) | **GET** /metrics/cpu | Get Cpu Metrics
[**get_healthcheck**](DataApi.md#get_healthcheck) | **GET** /healthz | Get Healthcheck
[**get_info**](DataApi.md#get_info) | **GET** /info | Get Info
[**get_latest_cpu_metrics**](DataApi.md#get_latest_cpu_metrics) | **GET** /metrics/cpu/latest | Get Latest Cpu Metrics
[**list_live_vms**](DataApi.md#list_live_vms) | **GET** /vm/live | List Live Vms
[**put_cpu_metric**](DataApi.md#put_cpu_metric) | **POST** /metrics/cpu | Put Cpu Metric
[**report_heartbeat**](DataApi.md#report_heartbeat) | **POST** /vm/heartbeat/{vm_id} | Report Heartbeat


# **get_auth_healthcheck**
> OkResponse get_auth_healthcheck()

Get Auth Healthcheck

Basic healthcheck that requires authentication

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.ok_response import OkResponse
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)

    try:
        # Get Auth Healthcheck
        api_response = api_instance.get_auth_healthcheck()
        print("The response of DataApi->get_auth_healthcheck:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_auth_healthcheck: %s\n" % e)
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

# **get_cpu_metrics**
> List[CpuMeasurement] get_cpu_metrics(vm_ids, from_ts=from_ts, to_ts=to_ts)

Get Cpu Metrics

Get cpu metrics for certain VMs between from_ts to to_ts, inclusive. :param vm_ids: A list of VM ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of CpuMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.cpu_measurement import CpuMeasurement
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)
    vm_ids = ['vm_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Cpu Metrics
        api_response = api_instance.get_cpu_metrics(vm_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_cpu_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_cpu_metrics: %s\n" % e)
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

# **get_healthcheck**
> OkResponse get_healthcheck()

Get Healthcheck

Basic healthcheck

### Example

```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.ok_response import OkResponse
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)

    try:
        # Get Healthcheck
        api_response = api_instance.get_healthcheck()
        print("The response of DataApi->get_healthcheck:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_healthcheck: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**OkResponse**](OkResponse.md)

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

# **get_info**
> InfoResponse get_info()

Get Info

Return basic info about deployment

### Example

```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.info_response import InfoResponse
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)

    try:
        # Get Info
        api_response = api_instance.get_info()
        print("The response of DataApi->get_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_info: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**InfoResponse**](InfoResponse.md)

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

# **get_latest_cpu_metrics**
> List[CpuMeasurement] get_latest_cpu_metrics(vm_ids)

Get Latest Cpu Metrics

Get the most recent CPU measurements for each VM

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.cpu_measurement import CpuMeasurement
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)
    vm_ids = ['vm_ids_example'] # List[str] | 

    try:
        # Get Latest Cpu Metrics
        api_response = api_instance.get_latest_cpu_metrics(vm_ids)
        print("The response of DataApi->get_latest_cpu_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_cpu_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vm_ids** | [**List[str]**](str.md)|  | 

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

# **list_live_vms**
> List[str] list_live_vms()

List Live Vms

Return a list of the active VMs

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)

    try:
        # List Live Vms
        api_response = api_instance.list_live_vms()
        print("The response of DataApi->list_live_vms:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->list_live_vms: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

**List[str]**

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

# **put_cpu_metric**
> OkResponse put_cpu_metric(cpu_measurement)

Put Cpu Metric

Put a cpu metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.cpu_measurement import CpuMeasurement
from centrality_controlplane_sdk.models.ok_response import OkResponse
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)
    cpu_measurement = centrality_controlplane_sdk.CpuMeasurement() # CpuMeasurement | 

    try:
        # Put Cpu Metric
        api_response = api_instance.put_cpu_metric(cpu_measurement)
        print("The response of DataApi->put_cpu_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_cpu_metric: %s\n" % e)
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

# **report_heartbeat**
> OkResponse report_heartbeat(vm_id)

Report Heartbeat

Report a heartbeat for a VM

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.ok_response import OkResponse
from centrality_controlplane_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = centrality_controlplane_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = centrality_controlplane_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = centrality_controlplane_sdk.DataApi(api_client)
    vm_id = 'vm_id_example' # str | 

    try:
        # Report Heartbeat
        api_response = api_instance.report_heartbeat(vm_id)
        print("The response of DataApi->report_heartbeat:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->report_heartbeat: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vm_id** | **str**|  | 

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
