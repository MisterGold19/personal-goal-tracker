from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str

    ENV: str
    APP_VERSION: str
    LOG_LEVEL: str
    DATABASE_URL: str

    # can be None to run on Github actions

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-arg]
