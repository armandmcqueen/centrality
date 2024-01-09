from rapidui.library.flexbox import CardContents, BaseCard


class NetThroughputCardContents(CardContents):
    interface_name: str
    sent_mbps: float
    recv_mbps: float


# TODO: This is pretty hacky, but it's not worth figuring out a better approach
# let's say max is 100 Gbit/s
MAX_THROUGHPUT = 100 * 1000 / 8


class NetThroughputCard(BaseCard):
    def __init__(self, parent_container, contents: NetThroughputCardContents):
        self.container = parent_container
        self.contents = contents

        sent_usage_percent = min(contents.sent_mbps / MAX_THROUGHPUT, 1)
        recv_usage_percent = min(contents.recv_mbps / MAX_THROUGHPUT, 1)
        self.iface_text = self.container.markdown(f"`{contents.interface_name}`")
        self.sent_progress = self.container.progress(sent_usage_percent)
        self.sent_text = self.container.markdown(
            f"Sent: {round(contents.sent_mbps, 3)} MiB/s"
        )
        self.recv_progress = self.container.progress(recv_usage_percent)
        self.recv_text = self.container.markdown(
            f"Recv: {round(contents.recv_mbps, 3)} MiB/s"
        )

    def empty(self):
        self.container.empty()
        self.iface_text.empty()
        self.sent_progress.empty()
        self.recv_progress.empty()
        self.sent_text.empty()
        self.recv_text.empty()

    def update(self, contents: NetThroughputCardContents):
        self.contents = contents
        sent_usage_percent = min(contents.sent_mbps / MAX_THROUGHPUT, 1)
        recv_usage_percent = min(contents.recv_mbps / MAX_THROUGHPUT, 1)
        self.iface_text.markdown(f"`{contents.interface_name}`")
        self.sent_progress.progress(sent_usage_percent)
        self.sent_text.markdown(f"Sent: {round(contents.sent_mbps, 3)} MiB/s")
        self.recv_progress.progress(recv_usage_percent)
        self.recv_text.markdown(f"Recv: {round(contents.recv_mbps, 3)} MiB/s")
