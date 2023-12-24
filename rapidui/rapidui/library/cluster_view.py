from rapidui.library.flexbox import CardContents, BaseCard


class MachineOverviewCardContents(CardContents):
    vm_id: str
    avg_cpu: float


class MachineOverviewCard(BaseCard):
    def __init__(self, parent_container, contents: MachineOverviewCardContents):
        self.parent = parent_container
        self.contents = contents

        self.title = self.parent.empty()
        self.title.write(f"{self.contents.vm_id}")
        self.progress = self.parent.progress(self.contents.avg_cpu / 100, text=f"{int(self.contents.avg_cpu)}%")

    def empty(self):
        self.parent.empty()
        self.title.empty()
        self.progress.empty()

    def update(self, contents: MachineOverviewCardContents):
        self.contents = contents
        self.title.write(f"{self.contents.vm_id}")
        self.progress.progress(self.contents.avg_cpu / 100, text=f"{int(self.contents.avg_cpu)}%")


class LiveMachineCount:
    def __init__(self, parent_container, machine_type: str, num_machines: int):
        self.parent = parent_container
        self.machine_type = machine_type
        self.num_machines = num_machines
        self.machine_count_container = self.parent.empty()
        # We need to set the background color of the container to match the main background color if
        # we don't want to highlight it as a card
        self.machine_count_container.markdown(
            self._gen_markdown(machine_type, num_machines),
            unsafe_allow_html=True,
        )

    def _gen_markdown(self, machine_type: str, num_machines: int):
        return f"""
            <div style='background-color: #1B2635'>
                <h3 style='text-align: center;'>{num_machines}</h3>
                <p style='text-align: center;'>{machine_type} Machines</p>
                <br/>
            <div>
            """

    def update(self, num_machines: int):
        self.num_machines = num_machines
        self.machine_count_container.markdown(
            self._gen_markdown(self.machine_type, self.num_machines),
            unsafe_allow_html=True,
        )


