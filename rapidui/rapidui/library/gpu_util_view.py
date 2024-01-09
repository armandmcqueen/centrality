from rapidui.library.flexbox import CardContents, BaseCard


class GpuUtilCardContents(CardContents):
    gpu_id: int
    curr_gpu: float


class GpuUtilCard(BaseCard):
    def __init__(self, parent_container, contents: GpuUtilCardContents):
        self.container = parent_container
        self.contents = contents
        self.progress = self.container.progress(contents.curr_gpu / 100)

    def empty(self):
        self.container.empty()
        self.progress.empty()

    def update(self, contents: GpuUtilCardContents):
        self.contents = contents
        self.progress.progress(contents.curr_gpu / 100)
