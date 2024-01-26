
from pydantic import BaseModel
from rich import Console
from common.sdks.controlplane.sdk import get_sdk, ControlPlaneSdkConfig
from common import constants
from centrality_controlplane_sdk import DataApi


class RawData(BaseModel):
    """
    This is the base class for raw data collected from the API so that the structure of the data
    is explicit.

    This should be subclassed for each subclass of DataVisualizerPipeline.
    """

    pass


class TransformedData(BaseModel):
    """
    This is the base class for the output of the raw data transformation step.

    The output of the data transformation step should create the exact data that will be presented to the user.

    This should be subclassed for each subclass of DataVisualizerPipeline.
    """

    pass


class DataVisualizerPipeline:
    """
    Base class for construction data visualization pipelines.

    Data visualization pipelines are composed of three steps:
    1. Collect raw data from the API (or other sources in rare cases)
    2. Transform the raw data into the data that will be presented to the user. Examples of
       this include averaging CPU usage over a time period, or filtering out data that is
       not relevant to the user if that can't be done at data retrieval time.
    3. Visualize the transformed data using rich.

    """

    CONTROL_PLANE_HOST = "localhost"
    CONTROL_PLANE_PORT = 8000
    CONTROL_PLANE_HTTPS = False

    def __init__(self):
        self.console = Console()
        self.control_plane_config = ControlPlaneSdkConfig(
            host=self.CONTROL_PLANE_HOST,
            port=self.CONTROL_PLANE_PORT,
            https=self.CONTROL_PLANE_HTTPS,
        )
        self.data_api: DataApi = get_sdk(
            self.control_plane_config, constants.CONTROL_PLANE_SDK_DEV_TOKEN
        )

    def collect_raw_data(self) -> RawData:
        """
        Collect all the raw data necessary to create a visualization that satisfies what the user asked for.
        """
        pass

    def transform_raw_data(self, raw_data: RawData) -> TransformedData:
        """
        Transform the raw data into the data that will be presented to the user.
        """
        pass

    def visualize_data(self, transformed_data: TransformedData):
        """
        Visualize the transformed data using rich.
        """
        pass
