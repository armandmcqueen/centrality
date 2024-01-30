from datetime import datetime, timedelta
import centrality_controlplane_sdk
from centrality_controlplane_sdk.rest import ApiException
from rich.console import Console
from rich.table import Table

# Configuration for the SDK to point to the correct URL and use the provided token for authentication
configuration = centrality_controlplane_sdk.Configuration(
    host="https://centrality-dev.fly.dev:8000"
)
configuration.access_token = "dev"


# Added this class to make it valid python
class DataVisualizer:
    @property
    def data_api(self) -> centrality_controlplane_sdk.DataApi:
        raise NotImplementedError()

    def collect_data(self):
        raise NotImplementedError()

    def visualize_data(self):
        raise NotImplementedError()


class AverageCpuDataVisualizer(DataVisualizer):
    def __init__(self):
        with centrality_controlplane_sdk.ApiClient(configuration) as api_client:
            self._data_api = centrality_controlplane_sdk.DataApi(api_client)

    @property
    def data_api(self) -> centrality_controlplane_sdk.DataApi:
        return self._data_api

    # edit to add return type
    def collect_data(self) -> dict[str, float]:
        # Obtain the current UTC time and compute the time 30 seconds ago
        current_time = datetime.utcnow()
        past_time = current_time - timedelta(seconds=30)
        try:
            live_machines = self.data_api.get_live_machines()
            print("Fetched list of live machines.")
            machine_data = {}

            for machine in live_machines:
                machine_id = machine.machine_id
                # Fetch the latest CPU metrics for each machine
                cpu_metrics = self.data_api.get_cpu_metrics(
                    [machine_id], from_ts=past_time, to_ts=current_time
                )
                print(f"Fetched CPU metrics for machine ID: {machine_id}")

                # Calculate average CPU usage for each machine
                if cpu_metrics:
                    avg_cpu_usage = sum(
                        [
                            sum(measurement.cpu_percents)
                            / len(measurement.cpu_percents)
                            for measurement in cpu_metrics
                        ]
                    ) / len(cpu_metrics)
                    machine_data[machine_id] = avg_cpu_usage
                else:
                    machine_data[machine_id] = "No Data"

            return machine_data
        except ApiException as e:
            print(f"Exception when calling DataApi: {str(e)}")
            return {}

    def visualize_data(self):
        data = self.collect_data()

        # Create a rich table to show the data
        table = Table(title="Average CPU Usage Per Machine (Last 30 seconds)")
        table.add_column("Machine ID", justify="left")
        table.add_column("Average CPU Usage (%)", justify="right")

        for machine_id, avg_cpu in data.items():
            table.add_row(machine_id, str(avg_cpu))

        # Print the table using Rich
        console = Console()
        console.print(table)


# Run the visualizer
visualizer = AverageCpuDataVisualizer()
visualizer.visualize_data()