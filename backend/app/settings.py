from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    vroom_url: str = "http://localhost:3000"
    vroom_timeout: int = 30 # seconds
    osrm_url: str = "http://localhost:5001"
    cors_origins: list[str] = ["http://localhost:5173"]
    nominatim_url: str = "https://nominatim.openstreetmap.org"
    nominatim_user_agent: str = "route-planner/0.1 (learning project)"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()