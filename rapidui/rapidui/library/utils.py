from rapidui.library.config import StreamlitUiConfig
import time


def calculate_epoch(interval_ms: int) -> int:
    # Given the current time in seconds, calculate the epoch in milliseconds. This is used in combination with
    # st.cache_data to refresh the cache every interval_ms milliseconds. This works because st.cache_data
    # caches based on argument values, so if we use the epoch as an argument to the cached function, it will
    # use the cache until the epoch updates.
    current_sec = int(time.time() * 1000)
    return int(current_sec / interval_ms)


def load_config() -> StreamlitUiConfig:
    return StreamlitUiConfig.from_envvar()
