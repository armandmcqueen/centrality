# centrality_controlplane_sdk.DataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_auth_healthcheck**](DataApi.md#get_auth_healthcheck) | **GET** /healthz/auth | Get Auth Healthcheck
[**get_cpu_metrics**](DataApi.md#get_cpu_metrics) | **GET** /machine/metrics/cpu | Get Cpu Metrics
[**get_disk_iops_metrics**](DataApi.md#get_disk_iops_metrics) | **GET** /machine/metrics/disk-iops | Get Disk Iops Metrics
[**get_disk_throughput_metrics**](DataApi.md#get_disk_throughput_metrics) | **GET** /machine/metrics/disk-throughput | Get Disk Throughput Metrics
[**get_disk_usage_metrics**](DataApi.md#get_disk_usage_metrics) | **GET** /machine/metrics/disk-usage | Get Disk Usage Metrics
[**get_gpu_memory_metrics**](DataApi.md#get_gpu_memory_metrics) | **GET** /machine/metrics/gpu-memory | Get Gpu Memory Metrics
[**get_gpu_utilization_metrics**](DataApi.md#get_gpu_utilization_metrics) | **GET** /machine/metrics/gpu-utilization | Get Gpu Utilization Metrics
[**get_healthcheck**](DataApi.md#get_healthcheck) | **GET** /healthz | Get Healthcheck
[**get_info**](DataApi.md#get_info) | **GET** /info | Get Info
[**get_latest_cpu_metrics**](DataApi.md#get_latest_cpu_metrics) | **GET** /machine/metrics/cpu/latest | Get Latest Cpu Metrics
[**get_latest_disk_iops_metrics**](DataApi.md#get_latest_disk_iops_metrics) | **GET** /machine/metrics/disk-iops/latest | Get Latest Disk Iops Metrics
[**get_latest_disk_throughput_metrics**](DataApi.md#get_latest_disk_throughput_metrics) | **GET** /machine/metrics/disk-throughput/latest | Get Latest Disk Throughput Metrics
[**get_latest_disk_usage_metrics**](DataApi.md#get_latest_disk_usage_metrics) | **GET** /machine/metrics/disk-usage/latest | Get Latest Disk Usage Metrics
[**get_latest_gpu_memory_metrics**](DataApi.md#get_latest_gpu_memory_metrics) | **GET** /machine/metrics/gpu-memory/latest | Get Latest Gpu Memory Metrics
[**get_latest_gpu_utilization_metrics**](DataApi.md#get_latest_gpu_utilization_metrics) | **GET** /machine/metrics/gpu-utilization/latest | Get Latest Gpu Utilization Metrics
[**get_latest_memory_metrics**](DataApi.md#get_latest_memory_metrics) | **GET** /machine/metrics/memory/latest | Get Latest Memory Metrics
[**get_latest_network_throughput_metrics**](DataApi.md#get_latest_network_throughput_metrics) | **GET** /machine/metrics/network-throughput/latest | Get Latest Network Throughput Metrics
[**get_latest_nvidia_smi_metrics**](DataApi.md#get_latest_nvidia_smi_metrics) | **GET** /machine/metrics/nvidia-smi/latest | Get Latest Nvidia Smi Metrics
[**get_live_machines**](DataApi.md#get_live_machines) | **GET** /machine/live | Get Live Machines
[**get_machine**](DataApi.md#get_machine) | **GET** /machine/{machine_id} | Get Machine
[**get_memory_metrics**](DataApi.md#get_memory_metrics) | **GET** /machine/metrics/memory | Get Memory Metrics
[**get_network_throughput_metrics**](DataApi.md#get_network_throughput_metrics) | **GET** /machine/metrics/network-throughput | Get Network Throughput Metrics
[**get_nvidia_smi_metrics**](DataApi.md#get_nvidia_smi_metrics) | **GET** /machine/metrics/nvidia-smi | Get Nvidia Smi Metrics
[**put_cpu_metric**](DataApi.md#put_cpu_metric) | **POST** /machine/metrics/cpu | Put Cpu Metric
[**put_disk_iops_metric**](DataApi.md#put_disk_iops_metric) | **POST** /machine/metrics/disk-iops | Put Disk Iops Metric
[**put_disk_throughput_metric**](DataApi.md#put_disk_throughput_metric) | **POST** /machine/metrics/disk-throughput | Put Disk Throughput Metric
[**put_disk_usage_metric**](DataApi.md#put_disk_usage_metric) | **POST** /machine/metrics/disk-usage | Put Disk Usage Metric
[**put_gpu_memory_metric**](DataApi.md#put_gpu_memory_metric) | **POST** /machine/metrics/gpu-memory | Put Gpu Memory Metric
[**put_gpu_utilization_metric**](DataApi.md#put_gpu_utilization_metric) | **POST** /machine/metrics/gpu-utilization | Put Gpu Utilization Metric
[**put_memory_metric**](DataApi.md#put_memory_metric) | **POST** /machine/metrics/memory | Put Memory Metric
[**put_network_throughput_metric**](DataApi.md#put_network_throughput_metric) | **POST** /machine/metrics/network-throughput | Put Network Throughput Metric
[**put_nvidia_smi_metric**](DataApi.md#put_nvidia_smi_metric) | **POST** /machine/metrics/nvidia-smi | Put Nvidia Smi Metric
[**register_machine**](DataApi.md#register_machine) | **POST** /machine/{machine_id}/register | Register Machine
[**report_machine_death**](DataApi.md#report_machine_death) | **POST** /machine/{machine_id}/report-death | Report Machine Death
[**report_machine_heartbeat**](DataApi.md#report_machine_heartbeat) | **POST** /machine/{machine_id}/heartbeat | Report Machine Heartbeat


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
> List[CpuMeasurement] get_cpu_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Cpu Metrics

Get cpu metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of CpuMeasurement objects

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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Cpu Metrics
        api_response = api_instance.get_cpu_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_cpu_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_cpu_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
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

# **get_disk_iops_metrics**
> List[DiskIopsMeasurement] get_disk_iops_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Disk Iops Metrics

Get disk_iops metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of DiskIopsMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_iops_measurement import DiskIopsMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Disk Iops Metrics
        api_response = api_instance.get_disk_iops_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_disk_iops_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_disk_iops_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[DiskIopsMeasurement]**](DiskIopsMeasurement.md)

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

# **get_disk_throughput_metrics**
> List[DiskThroughputMeasurement] get_disk_throughput_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Disk Throughput Metrics

Get disk_throughput metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of DiskThroughputMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_throughput_measurement import DiskThroughputMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Disk Throughput Metrics
        api_response = api_instance.get_disk_throughput_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_disk_throughput_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_disk_throughput_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[DiskThroughputMeasurement]**](DiskThroughputMeasurement.md)

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

# **get_disk_usage_metrics**
> List[DiskUsageMeasurement] get_disk_usage_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Disk Usage Metrics

Get disk_usage metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of DiskUsageMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_usage_measurement import DiskUsageMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Disk Usage Metrics
        api_response = api_instance.get_disk_usage_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_disk_usage_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_disk_usage_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[DiskUsageMeasurement]**](DiskUsageMeasurement.md)

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

# **get_gpu_memory_metrics**
> List[GpuMemoryMeasurement] get_gpu_memory_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Gpu Memory Metrics

Get gpu_memory metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of GpuMemoryMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_memory_measurement import GpuMemoryMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Gpu Memory Metrics
        api_response = api_instance.get_gpu_memory_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_gpu_memory_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_gpu_memory_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[GpuMemoryMeasurement]**](GpuMemoryMeasurement.md)

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

# **get_gpu_utilization_metrics**
> List[GpuUtilizationMeasurement] get_gpu_utilization_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Gpu Utilization Metrics

Get gpu_utilization metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of GpuUtilizationMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_utilization_measurement import GpuUtilizationMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Gpu Utilization Metrics
        api_response = api_instance.get_gpu_utilization_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_gpu_utilization_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_gpu_utilization_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[GpuUtilizationMeasurement]**](GpuUtilizationMeasurement.md)

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
> List[CpuMeasurement] get_latest_cpu_metrics(machine_ids)

Get Latest Cpu Metrics

Get the most recent cpu measurements for each machine

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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Cpu Metrics
        api_response = api_instance.get_latest_cpu_metrics(machine_ids)
        print("The response of DataApi->get_latest_cpu_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_cpu_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

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

# **get_latest_disk_iops_metrics**
> List[DiskIopsMeasurement] get_latest_disk_iops_metrics(machine_ids)

Get Latest Disk Iops Metrics

Get the most recent disk_iops measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_iops_measurement import DiskIopsMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Disk Iops Metrics
        api_response = api_instance.get_latest_disk_iops_metrics(machine_ids)
        print("The response of DataApi->get_latest_disk_iops_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_disk_iops_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[DiskIopsMeasurement]**](DiskIopsMeasurement.md)

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

# **get_latest_disk_throughput_metrics**
> List[DiskThroughputMeasurement] get_latest_disk_throughput_metrics(machine_ids)

Get Latest Disk Throughput Metrics

Get the most recent disk_throughput measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_throughput_measurement import DiskThroughputMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Disk Throughput Metrics
        api_response = api_instance.get_latest_disk_throughput_metrics(machine_ids)
        print("The response of DataApi->get_latest_disk_throughput_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_disk_throughput_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[DiskThroughputMeasurement]**](DiskThroughputMeasurement.md)

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

# **get_latest_disk_usage_metrics**
> List[DiskUsageMeasurement] get_latest_disk_usage_metrics(machine_ids)

Get Latest Disk Usage Metrics

Get the most recent disk_usage measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_usage_measurement import DiskUsageMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Disk Usage Metrics
        api_response = api_instance.get_latest_disk_usage_metrics(machine_ids)
        print("The response of DataApi->get_latest_disk_usage_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_disk_usage_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[DiskUsageMeasurement]**](DiskUsageMeasurement.md)

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

# **get_latest_gpu_memory_metrics**
> List[GpuMemoryMeasurement] get_latest_gpu_memory_metrics(machine_ids)

Get Latest Gpu Memory Metrics

Get the most recent gpu_memory measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_memory_measurement import GpuMemoryMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Gpu Memory Metrics
        api_response = api_instance.get_latest_gpu_memory_metrics(machine_ids)
        print("The response of DataApi->get_latest_gpu_memory_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_gpu_memory_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[GpuMemoryMeasurement]**](GpuMemoryMeasurement.md)

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

# **get_latest_gpu_utilization_metrics**
> List[GpuUtilizationMeasurement] get_latest_gpu_utilization_metrics(machine_ids)

Get Latest Gpu Utilization Metrics

Get the most recent gpu_utilization measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_utilization_measurement import GpuUtilizationMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Gpu Utilization Metrics
        api_response = api_instance.get_latest_gpu_utilization_metrics(machine_ids)
        print("The response of DataApi->get_latest_gpu_utilization_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_gpu_utilization_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[GpuUtilizationMeasurement]**](GpuUtilizationMeasurement.md)

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

# **get_latest_memory_metrics**
> List[MemoryMeasurement] get_latest_memory_metrics(machine_ids)

Get Latest Memory Metrics

Get the most recent memory measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.memory_measurement import MemoryMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Memory Metrics
        api_response = api_instance.get_latest_memory_metrics(machine_ids)
        print("The response of DataApi->get_latest_memory_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_memory_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[MemoryMeasurement]**](MemoryMeasurement.md)

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

# **get_latest_network_throughput_metrics**
> List[NetworkThroughputMeasurement] get_latest_network_throughput_metrics(machine_ids)

Get Latest Network Throughput Metrics

Get the most recent network_throughput measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.network_throughput_measurement import NetworkThroughputMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Network Throughput Metrics
        api_response = api_instance.get_latest_network_throughput_metrics(machine_ids)
        print("The response of DataApi->get_latest_network_throughput_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_network_throughput_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[NetworkThroughputMeasurement]**](NetworkThroughputMeasurement.md)

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

# **get_latest_nvidia_smi_metrics**
> List[NvidiaSmiMeasurement] get_latest_nvidia_smi_metrics(machine_ids)

Get Latest Nvidia Smi Metrics

Get the most recent nvidia_smi measurements for each machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.nvidia_smi_measurement import NvidiaSmiMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 

    try:
        # Get Latest Nvidia Smi Metrics
        api_response = api_instance.get_latest_nvidia_smi_metrics(machine_ids)
        print("The response of DataApi->get_latest_nvidia_smi_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_latest_nvidia_smi_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 

### Return type

[**List[NvidiaSmiMeasurement]**](NvidiaSmiMeasurement.md)

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

# **get_live_machines**
> List[MachineInfo] get_live_machines()

Get Live Machines

Return a list of the active machines

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.machine_info import MachineInfo
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
        # Get Live Machines
        api_response = api_instance.get_live_machines()
        print("The response of DataApi->get_live_machines:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_live_machines: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**List[MachineInfo]**](MachineInfo.md)

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

# **get_machine**
> MachineInfo get_machine(machine_id)

Get Machine

Return

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.machine_info import MachineInfo
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
    machine_id = 'machine_id_example' # str | 

    try:
        # Get Machine
        api_response = api_instance.get_machine(machine_id)
        print("The response of DataApi->get_machine:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_machine: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_id** | **str**|  | 

### Return type

[**MachineInfo**](MachineInfo.md)

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

# **get_memory_metrics**
> List[MemoryMeasurement] get_memory_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Memory Metrics

Get memory metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of MemoryMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.memory_measurement import MemoryMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Memory Metrics
        api_response = api_instance.get_memory_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_memory_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_memory_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[MemoryMeasurement]**](MemoryMeasurement.md)

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

# **get_network_throughput_metrics**
> List[NetworkThroughputMeasurement] get_network_throughput_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Network Throughput Metrics

Get network_throughput metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of NetworkThroughputMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.network_throughput_measurement import NetworkThroughputMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Network Throughput Metrics
        api_response = api_instance.get_network_throughput_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_network_throughput_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_network_throughput_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[NetworkThroughputMeasurement]**](NetworkThroughputMeasurement.md)

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

# **get_nvidia_smi_metrics**
> List[NvidiaSmiMeasurement] get_nvidia_smi_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)

Get Nvidia Smi Metrics

Get nvidia_smi metrics for certain MACHINEs between from_ts to to_ts, inclusive. :param machine_ids: A list of machine ids to get metrics for. Empty list returns no results (but not an error). :param from_ts: Start time filter, inclusive. Optional. :param to_ts: End time filter, inclusive. Optional. If to_ts is before from_ts, there will not be an               error, but the results will be empty. :return: List of NvidiaSmiMeasurement objects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.nvidia_smi_measurement import NvidiaSmiMeasurement
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
    machine_ids = ['machine_ids_example'] # List[str] | 
    from_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    to_ts = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # Get Nvidia Smi Metrics
        api_response = api_instance.get_nvidia_smi_metrics(machine_ids, from_ts=from_ts, to_ts=to_ts)
        print("The response of DataApi->get_nvidia_smi_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_nvidia_smi_metrics: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_ids** | [**List[str]**](str.md)|  | 
 **from_ts** | **datetime**|  | [optional] 
 **to_ts** | **datetime**|  | [optional] 

### Return type

[**List[NvidiaSmiMeasurement]**](NvidiaSmiMeasurement.md)

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

# **put_disk_iops_metric**
> OkResponse put_disk_iops_metric(disk_iops_measurement)

Put Disk Iops Metric

Put a disk_iops metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_iops_measurement import DiskIopsMeasurement
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
    disk_iops_measurement = centrality_controlplane_sdk.DiskIopsMeasurement() # DiskIopsMeasurement | 

    try:
        # Put Disk Iops Metric
        api_response = api_instance.put_disk_iops_metric(disk_iops_measurement)
        print("The response of DataApi->put_disk_iops_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_disk_iops_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **disk_iops_measurement** | [**DiskIopsMeasurement**](DiskIopsMeasurement.md)|  | 

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

# **put_disk_throughput_metric**
> OkResponse put_disk_throughput_metric(disk_throughput_measurement)

Put Disk Throughput Metric

Put a disk_throughput metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_throughput_measurement import DiskThroughputMeasurement
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
    disk_throughput_measurement = centrality_controlplane_sdk.DiskThroughputMeasurement() # DiskThroughputMeasurement | 

    try:
        # Put Disk Throughput Metric
        api_response = api_instance.put_disk_throughput_metric(disk_throughput_measurement)
        print("The response of DataApi->put_disk_throughput_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_disk_throughput_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **disk_throughput_measurement** | [**DiskThroughputMeasurement**](DiskThroughputMeasurement.md)|  | 

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

# **put_disk_usage_metric**
> OkResponse put_disk_usage_metric(disk_usage_measurement)

Put Disk Usage Metric

Put a disk_usage metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.disk_usage_measurement import DiskUsageMeasurement
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
    disk_usage_measurement = centrality_controlplane_sdk.DiskUsageMeasurement() # DiskUsageMeasurement | 

    try:
        # Put Disk Usage Metric
        api_response = api_instance.put_disk_usage_metric(disk_usage_measurement)
        print("The response of DataApi->put_disk_usage_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_disk_usage_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **disk_usage_measurement** | [**DiskUsageMeasurement**](DiskUsageMeasurement.md)|  | 

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

# **put_gpu_memory_metric**
> OkResponse put_gpu_memory_metric(gpu_memory_measurement)

Put Gpu Memory Metric

Put a gpu_memory metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_memory_measurement import GpuMemoryMeasurement
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
    gpu_memory_measurement = centrality_controlplane_sdk.GpuMemoryMeasurement() # GpuMemoryMeasurement | 

    try:
        # Put Gpu Memory Metric
        api_response = api_instance.put_gpu_memory_metric(gpu_memory_measurement)
        print("The response of DataApi->put_gpu_memory_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_gpu_memory_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gpu_memory_measurement** | [**GpuMemoryMeasurement**](GpuMemoryMeasurement.md)|  | 

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

# **put_gpu_utilization_metric**
> OkResponse put_gpu_utilization_metric(gpu_utilization_measurement)

Put Gpu Utilization Metric

Put a gpu_utilization metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.gpu_utilization_measurement import GpuUtilizationMeasurement
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
    gpu_utilization_measurement = centrality_controlplane_sdk.GpuUtilizationMeasurement() # GpuUtilizationMeasurement | 

    try:
        # Put Gpu Utilization Metric
        api_response = api_instance.put_gpu_utilization_metric(gpu_utilization_measurement)
        print("The response of DataApi->put_gpu_utilization_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_gpu_utilization_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gpu_utilization_measurement** | [**GpuUtilizationMeasurement**](GpuUtilizationMeasurement.md)|  | 

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

# **put_memory_metric**
> OkResponse put_memory_metric(memory_measurement)

Put Memory Metric

Put a memory metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.memory_measurement import MemoryMeasurement
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
    memory_measurement = centrality_controlplane_sdk.MemoryMeasurement() # MemoryMeasurement | 

    try:
        # Put Memory Metric
        api_response = api_instance.put_memory_metric(memory_measurement)
        print("The response of DataApi->put_memory_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_memory_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **memory_measurement** | [**MemoryMeasurement**](MemoryMeasurement.md)|  | 

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

# **put_network_throughput_metric**
> OkResponse put_network_throughput_metric(network_throughput_measurement)

Put Network Throughput Metric

Put a network_throughput metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.network_throughput_measurement import NetworkThroughputMeasurement
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
    network_throughput_measurement = centrality_controlplane_sdk.NetworkThroughputMeasurement() # NetworkThroughputMeasurement | 

    try:
        # Put Network Throughput Metric
        api_response = api_instance.put_network_throughput_metric(network_throughput_measurement)
        print("The response of DataApi->put_network_throughput_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_network_throughput_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **network_throughput_measurement** | [**NetworkThroughputMeasurement**](NetworkThroughputMeasurement.md)|  | 

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

# **put_nvidia_smi_metric**
> OkResponse put_nvidia_smi_metric(nvidia_smi_measurement)

Put Nvidia Smi Metric

Put a nvidia_smi metric measurement into the datastore

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.nvidia_smi_measurement import NvidiaSmiMeasurement
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
    nvidia_smi_measurement = centrality_controlplane_sdk.NvidiaSmiMeasurement() # NvidiaSmiMeasurement | 

    try:
        # Put Nvidia Smi Metric
        api_response = api_instance.put_nvidia_smi_metric(nvidia_smi_measurement)
        print("The response of DataApi->put_nvidia_smi_metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->put_nvidia_smi_metric: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **nvidia_smi_measurement** | [**NvidiaSmiMeasurement**](NvidiaSmiMeasurement.md)|  | 

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

# **register_machine**
> OkResponse register_machine(machine_id, machine_registration_info)

Register Machine

Register a machine

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import centrality_controlplane_sdk
from centrality_controlplane_sdk.models.machine_registration_info import MachineRegistrationInfo
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
    machine_id = 'machine_id_example' # str | 
    machine_registration_info = centrality_controlplane_sdk.MachineRegistrationInfo() # MachineRegistrationInfo | 

    try:
        # Register Machine
        api_response = api_instance.register_machine(machine_id, machine_registration_info)
        print("The response of DataApi->register_machine:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->register_machine: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_id** | **str**|  | 
 **machine_registration_info** | [**MachineRegistrationInfo**](MachineRegistrationInfo.md)|  | 

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

# **report_machine_death**
> OkResponse report_machine_death(machine_id)

Report Machine Death

Report that a machine is dead, so that it is removed immediately.  This can be useful when you need the live list to update faster than the timeout.

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
    machine_id = 'machine_id_example' # str | 

    try:
        # Report Machine Death
        api_response = api_instance.report_machine_death(machine_id)
        print("The response of DataApi->report_machine_death:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->report_machine_death: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_id** | **str**|  | 

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

# **report_machine_heartbeat**
> OkResponse report_machine_heartbeat(machine_id)

Report Machine Heartbeat

Report a heartbeat for a machine

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
    machine_id = 'machine_id_example' # str | 

    try:
        # Report Machine Heartbeat
        api_response = api_instance.report_machine_heartbeat(machine_id)
        print("The response of DataApi->report_machine_heartbeat:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->report_machine_heartbeat: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_id** | **str**|  | 

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

