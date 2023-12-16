from common.config.config import CentralityConfig


class VmAgentRestConfig(CentralityConfig):
    port: int = 7777
    startup_healthcheck_timeout: int = 20
    startup_healthcheck_poll_interval: float = 0.5

