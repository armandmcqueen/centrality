from rapidui.library.flexbox import CardContents, BaseCard


class GpuMemCardContents(CardContents):
    gpu_id: int
    used_mem: float
    total_mem: float


class GpuMemCard(BaseCard):
    def __init__(self, parent_container, contents: GpuMemCardContents):
        self.container = parent_container
        self.contents = contents
        usage_percent = contents.used_mem / contents.total_mem
        self.progress = self.container.progress(usage_percent)
        self.text = self.container.markdown(
            f"{int(contents.used_mem)} MiB / {int(contents.total_mem)} MiB"
        )
        # TODO: Add text

    def empty(self):
        self.container.empty()
        self.progress.empty()

    def update(self, contents: GpuMemCardContents):
        self.contents = contents
        usage_percent = contents.used_mem / contents.total_mem
        self.progress.progress(usage_percent)
        self.text.markdown(
            f"{int(contents.used_mem)} MiB / {int(contents.total_mem)} MiB"
        )
