import time
import random
from rapidui.lib.cpu_view import CpuCard, CpuCardContents
from rapidui.lib.flexbox import UniformFlexbox
from rapidui.header import header
from rapidui.lib.utils import load_config

def main():
    config = load_config()
    header("Machine CPUs", disable_card_fill=True)

    start_time = time.time()

    def gen_data() -> list[CpuCardContents]:
        # swap between 8 and 16 cpus every 5 seconds
        if (time.time() - start_time) % 10 < 5:
            return [CpuCardContents(i, random.random() * 100) for i in range(32)]
        else:
            return [CpuCardContents(i, random.random() * 100) for i in range(64)]

    flexbox = UniformFlexbox(4, CpuCard, border=False)
    flexbox.set_initial_cards(gen_data())

    while True:
        new_data = gen_data()
        flexbox.update_cards(new_data)
        time.sleep(0.1)


main()