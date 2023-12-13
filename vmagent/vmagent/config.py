from pydantic import BaseModel


class VmAgentConfig(BaseModel):
    vm_id: str


