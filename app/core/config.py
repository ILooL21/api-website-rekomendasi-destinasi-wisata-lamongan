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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application Settings
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = True

    # CORS Settings
    ALLOWED_HOSTS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]
    ALLOWED_CREDENTIALS: bool = True

settings = Settings()
