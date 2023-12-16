from common.config.config import CentralityConfig


class ControlPlaneSdkConfig(CentralityConfig):
    host: str = "localhost"
    port: int = 8000
    https: bool = False
