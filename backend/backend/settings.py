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
    CORS_ORIGIN: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "https://test.d22pi7rog234uz.amplifyapp.com",
    ]

    # AI Settings
    ## number of words to use for the context
    SEGMENT_CHUNK_SIZE: int = 64
    TEXT_ENDPOINT: str = "arn:aws:comprehend:us-east-1:087582090241:document-classifier-endpoint/toxic-comments-endpoint"
    VIDEO_REKOGNITION_TIMEOUT: int = 60 * 10  # 10 minutes

    # S3 Settings
    S3_BUCKET_NAME: str = "buyaomafandata"

    # Integrations
    ## Telegram
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str

    class Config:
        env_file = ".env.prod"


@lru_cache()
def get_settings():
    return Settings()
