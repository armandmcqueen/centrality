from common.config.config import CentralityConfig


class ControlPlaneRestConfig(CentralityConfig):
    port: int = 8000
    startup_healthcheck_timeout: int = 20
    startup_healthcheck_poll_interval: float = 0.5



