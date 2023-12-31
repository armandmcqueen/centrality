import time
import requests
from rich import print


# Error if healthcheck endpoint is not reachable within timeout
class HealthcheckTimeoutError(Exception):
    pass


HealthcheckSucceededBool = bool


# TODO: Is this worth keeping around? It doesn't use the SDK, which is useful in some ways
def wait_for_healthy(
    healthcheck_url: str,
    startup_healthcheck_timeout: int,
    startup_healthcheck_poll_interval: float = 0.5,
    log_progress: bool = False,
    suppress_error: bool = False,
) -> HealthcheckSucceededBool:
    """Query the healthcheck endpoint until either it returns a 200 or we timeout."""

    log = print if log_progress else lambda *a, **k: None

    start_time = time.time()
    max_time = start_time + startup_healthcheck_timeout
    while time.time() < max_time:
        try:
            response = requests.get(healthcheck_url, timeout=0.5)
            if response.status_code == 200:
                log("✅  API is healthy")
                return True
        except requests.exceptions.ConnectionError:
            log(f"⏳  ConnectionError when trying to connect to {healthcheck_url}")
        except requests.exceptions.ReadTimeout:
            log(f"⌛️ ReadTimeout when trying to connect to {healthcheck_url}")
        time.sleep(startup_healthcheck_poll_interval)

    if not suppress_error:
        raise HealthcheckTimeoutError(
            f"Healthcheck didn't pass within {startup_healthcheck_timeout} seconds"
        )
    return False
