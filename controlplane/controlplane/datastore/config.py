from dataclasses import dataclass


@dataclass
class DatastoreConfig:
    host: str
    port: str
    username: str
    password: str
    verbose_orm: bool

    def get_url(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}"


class DefaultDatastoreConfig(DatastoreConfig):
    def __init__(self):
        super().__init__(
            host="localhost",
            port="5432",
            username="postgres",
            password="postgres",
            verbose_orm=False,
        )
