from rich.live import Live


class MetricCollector:
    """Interface for metric collectors"""

    def collect(self):
        pass

    def collect_and_render(self, live: Live):
        pass

    def shutdown(self):
        pass
