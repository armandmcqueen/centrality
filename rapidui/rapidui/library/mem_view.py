from rapidui.library.flexbox import CardContents, BaseCard


class MemCardContents(CardContents):
    free_mem: float
    total_mem: float


class MemCard(BaseCard):
    def __init__(self, parent_container, contents: MemCardContents):
        self.container = parent_container
        self.contents = contents
        used_mem = contents.total_mem - contents.free_mem
        usage_percent = used_mem / contents.total_mem
        self.progress = self.container.progress(usage_percent)
        self.text = self.container.empty()
        self.text.markdown(
            f"{int(used_mem)} MiB / {int(contents.total_mem)} MiB (free: {int(contents.free_mem)} MiB)"
        )

    def empty(self):
        self.container.empty()
        self.progress.empty()

    def update(self, contents: MemCardContents):
        self.contents = contents
        used_mem = contents.total_mem - contents.free_mem
        usage_percent = used_mem / contents.total_mem
        self.progress.progress(usage_percent)
        self.text.markdown(
            f"{int(used_mem)} MiB / {int(contents.total_mem)} MiB (free: {int(contents.free_mem)} MiB)"
        )
