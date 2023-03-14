from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # AWS Credentials
    # should be automatically loaded from environment variables
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SESSION_TOKEN: Optional[str] = None

    # CORS Settings
    # '["http://localhost:3000"]' is the default value
    CORS_ORIGIN: List[AnyHttpUrl] = ["http://localhost:3000"]

    # S3 Settings
    S3_BUCKET_NAME: str = "data"


@lru_cache()
def get_settings():
    return Settings()
