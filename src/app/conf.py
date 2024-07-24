import dotenv
import os

dotenv.load_dotenv("./.env")

__all__ = [
    "DBconf",
]


class DBconf:
    DB_DRIVER = os.getenv("DB_DRIVER", "asyncpg")
    DB = os.getenv("DB", "postgresql")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_NAME = os.getenv("DB_NAME", "projectx")
    DB_TEST_NAME = os.getenv("DB_TEST_NAME", "test")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
    PROD_DB = "postgresql+asyncpg://postgres:admin@host.docker.internal:5432/projectx"

    @property
    def get_db_url(self) -> str:
        """
        ссылка на базу данных для подключения через sqlachemy
        """
        return f"{self.DB}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_db_url_migration(self) -> str:
        return f"{self.DB}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_db_url_test(self) -> str:
        return f"{self.DB}+{self.DB_DRIVER}://postgres:admin@localhost:5433/test"


DBconfinit = DBconf()
