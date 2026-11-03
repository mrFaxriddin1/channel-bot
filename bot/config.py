from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    database_url: str
    required_channel: str
    admin_id: int
    timezone: str = "Asia/Tashkent"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
