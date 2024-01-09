from rapidui.library.flexbox import CardContents, BaseCard


class DiskUsageCardContents(CardContents):
    disk_name: str
    used_mb: float
    total_mb: float


class DiskUsageCard(BaseCard):
    def __init__(self, parent_container, contents: DiskUsageCardContents):
        self.container = parent_container
        self.contents = contents
        usage_percent = contents.used_mb / contents.total_mb
        self.header_text = self.container.empty()
        self.header_text.markdown(f"`{contents.disk_name}`")
        self.progress = self.container.progress(usage_percent)
        self.text = self.container.empty()
        self.text.markdown(
            f"{int(contents.used_mb)} MiB / {int(contents.total_mb)} MiB"
        )

    def empty(self):
        self.container.empty()
        self.progress.empty()
        self.header_text.empty()
        self.text.empty()

    def update(self, contents: DiskUsageCardContents):
        self.contents = contents
        usage_percent = contents.used_mb / contents.total_mb
        self.progress.progress(usage_percent)
        self.header_text.markdown(f"`{contents.disk_name}`")
        self.text.markdown(
            f"{int(contents.used_mb)} MiB / {int(contents.total_mb)} MiB"
        )
