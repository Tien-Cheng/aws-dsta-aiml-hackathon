from functools import lru_cache
from typing import Optional, List

from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    # AWS Credentials
    # should be automatically loaded from environment variables
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: Optional[str] = None

    # CORS Settings
    # '["http://localhost:3000"]' is the default value
    CORS_ORIGIN: List[AnyHttpUrl] = ["http://localhost:3000"]


@lru_cache()
def get_settings():
    return Settings()