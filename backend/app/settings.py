from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    vroom_url: str = "http://localhost:3000"
    vroom_timeout: int = 30 # seconds
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env__file=".env")

settings = Settings()