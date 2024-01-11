from rapidui.library.flexbox import CardContents, BaseCard


class NvidiaSmiCardContents(CardContents):
    output: str


class NvidiaSmiCard(BaseCard):
    def __init__(self, parent_container, contents: NvidiaSmiCardContents):
        self.container = parent_container
        self.contents = contents
        self.text = self.container.empty()
        self.text.markdown(f"```\n{contents.output}\n```")

    def empty(self):
        self.text.empty()
        self.container.empty()

    def update(self, contents: NvidiaSmiCardContents):
        self.contents = contents
        self.text.markdown(f"```\n{contents.output}\n```")
