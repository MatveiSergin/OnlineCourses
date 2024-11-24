from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_DIALECT: str = "postgresql"
    DB_DRIVER: str = "asyncpg"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "example"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DATABASE: str = "online_courses"
    AUTH_SECRET: str = "auth_secret"
    AUTH_RESET_SECRET: str = "auth_reset_secret"
    ENGINE_ECHO: bool = True
    ENGINE_POOL_SIZE: int = 10
    PATH_TO_REQUEST_LOG: str = "logs/AuthServiceRequests.log"
    PATH_TO_DATABASE_LOG: str = "logs/AuthServiceDatabase.log"
    FILE_SERVICE_URL: str = "http://mock_url"
    @property
    def DATABASE_URL(self):
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE}"

    model_config = SettingsConfigDict(env_file="settings/.env")


settings = Settings()
