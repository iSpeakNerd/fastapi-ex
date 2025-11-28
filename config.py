from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import List, Literal
import json
from pathlib import Path

# Load environment variables from .env
# Get root directory
BASE_DIR = Path(__file__).parents[0]


# keys must match values provided in .env
class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI example"

    DEV_USER: str = "dev"
    DEV_EMAIL: str = "dev@example.com"
    DEV_USER_ID: str = "001"

    # CORS with fallback defaults
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://example.com",
    ]

    ENV: Literal["development", "testing", "production"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # OpenAI
    OPENAI_API_KEY: str

    # use env file location in root if it exists (development)
    model_config = SettingsConfigDict(
        env_file=".env.local" if (BASE_DIR / ".env.local").exists() else None
    )

    @staticmethod
    def show() -> None:
        settings = Settings()
        settings_dict = settings.model_dump()
        if settings.ENV == "development":
            for key, value in settings_dict.items():
                if "API" in key or "PROMPT" in key:
                    print(f"{key} = {value[:12]}...\n")
                else:
                    print(f"{key} = {value}\n")
        else:
            pass


# debug
if __name__ == "__main__":
    s = Settings()
    s.show()
