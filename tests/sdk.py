import datetime

import controlplane_sdk
from controlplane_sdk.rest import ApiException
from controlplane_sdk.models import CpuMeasurement


configuration = controlplane_sdk.Configuration(
    access_token="dev",
    host="http://localhost:8000",
)


# Enter a context with an instance of the API client
with controlplane_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = controlplane_sdk.MainApi(api_client)

    try:
        vms = api_instance.list_vms()
        measurement = CpuMeasurement(
            vm_id="vm1",
            ts=datetime.datetime.now(datetime.timezone.utc),
            cpu_percents=[1, 2, 3],
        )
        api_instance.put_cpu_metric(measurement)
        # print(vms)
    except ApiException as e:
        print("Exception when calling MainApi->ListVms: %s\n" % e)
