from rapidui.library.config import StreamlitUiConfig
import time


def calculate_epoch(interval_ms: int) -> int:
    current_sec = int(time.time() * 1000)
    return int(current_sec / interval_ms)


def load_config() -> StreamlitUiConfig:
    return StreamlitUiConfig.from_envvar()
