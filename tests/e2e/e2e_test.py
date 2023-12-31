# test_feature_a.py
import requests  # noqa

from common.utils.wait_for_healthy import wait_for_healthy


def test_api_endpoint(docker_compose):
    """
    A sample e2e test that checks if an API endpoint is responding correctly.
    Assumes that one of the Docker containers exposes an API.
    """

    # Example URL (adjust based on your application's endpoint)
    url = "http://localhost:8000/healthz"

    wait_for_healthy(
        healthcheck_url=url,
        startup_healthcheck_timeout=120,
        startup_healthcheck_poll_interval=0.5,
        log_progress=True,
        suppress_error=False,
    )
