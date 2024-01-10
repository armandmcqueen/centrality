from rapidui.library.flexbox import CardContents, BaseCard


class DiskIoCardContents(CardContents):
    disk_name: str
    write_mbps: float
    read_mbps: float
    iops: float


class DiskIoCard(BaseCard):
    def __init__(self, parent_container, contents: DiskIoCardContents):
        self.container = parent_container
        self.contents = contents
        self.disk_name = self.container.markdown(f"`{contents.disk_name}`")
        self.read_text = self.container.markdown(
            f"Read: {round(contents.read_mbps, 2)} MiB/s"
        )
        self.write_text = self.container.markdown(
            f"Write: {round(contents.write_mbps, 2)} MiB/s"
        )
        self.iops_text = self.container.markdown(f"IOPS: {round(contents.iops, 2)}")

    def empty(self):
        self.container.empty()
        self.disk_name.empty()
        self.read_text.empty()
        self.write_text.empty()
        self.iops_text.empty()

    def update(self, contents: DiskIoCardContents):
        self.contents = contents
        self.disk_name.markdown(f"`{contents.disk_name}`")
        self.read_text.markdown(f"Read: {round(contents.read_mbps, 2)} MiB/s")
        self.write_text.markdown(f"Write: {round(contents.write_mbps, 2)} MiB/s")
        self.iops_text.markdown(f"IOPS: {round(contents.iops, 2)}")
