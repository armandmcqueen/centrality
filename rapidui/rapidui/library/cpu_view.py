
from rapidui.library.flexbox import CardContents, BaseCard


class CpuCardContents(CardContents):
    def __init__(self, cpu_id: int, curr_cpu: float):
        self.cpu_id = cpu_id
        self.curr_cpu = curr_cpu


class CpuCard(BaseCard):
    def __init__(self, parent_container, contents: CpuCardContents):
        self.container = parent_container
        self.contents = contents
        self.progress = self.container.progress(contents.curr_cpu / 100)

    def empty(self):
        self.container.empty()
        self.progress.empty()

    def update(self, contents: CpuCardContents):
        self.contents = contents
        self.progress.progress(contents.curr_cpu / 100)

