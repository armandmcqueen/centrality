from rich.live import Live


class MetricSampler:
    """Interface for metric collectors"""

    def sample(self):
        pass

    def sample_and_render(self, live: Live):
        pass

    def shutdown(self):
        pass
