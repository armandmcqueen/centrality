from pydantic import BaseModel


class ControlPlaneSdkConfig(BaseModel):
    host: str
    port: int
    https: bool


class DefaultControlPlaneSdkConfig(ControlPlaneSdkConfig):
    host: str = "localhost"
    port: int = 8000
    https: bool = False

