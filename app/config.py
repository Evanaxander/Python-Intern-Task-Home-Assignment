from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./app.db", alias="DATABASE_URL")
    user_agent: str = Field(default="SMS-Scraper/1.0 (+https://example.invalid)", alias="USER_AGENT")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "populate_by_name": True,
    }

settings = Settings()
