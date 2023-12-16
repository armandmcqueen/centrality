from common.config.config import CentralityConfig


class DatastoreConfig(CentralityConfig):
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    verbose_orm: bool = False

    def get_url(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}"
