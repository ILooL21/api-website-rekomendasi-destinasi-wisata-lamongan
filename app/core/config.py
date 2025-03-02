from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env" , env_file_encoding="utf-8" ,extra="allow")

    # Database Config
    DB_ENGINE: str = "postgresql"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "mydatabase"

    @property
    def database_url(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Security Config
    SECRET_KEY: str = "defaultsecretkey"
    ALGORITHM: str = "HS256"
    DEBUG: bool = True

settings = Settings()
