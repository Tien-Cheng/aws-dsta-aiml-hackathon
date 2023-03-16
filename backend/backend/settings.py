from functools import lru_cache
from typing import Dict, List, Optional, Set

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # AWS Credentials
    # should be automatically loaded from environment variables
    AWS_DEFAULT_REGION: str = "us-east-1"
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
    API_RETRY_ATTEMPTS: int = 10

    # S3 Settings
    S3_BUCKET_NAME: str = "buyaomafandata"

    # Class processing
    MIN_CONFIDENCE: float = 0.5
    ACCEPTED_TOXICITY_CLASSES: Optional[Set[str]] = {
        "toxic",
        "severe_toxic",
        "obscene",
        "threat",
        "insult",
        "identity_hate",
        "non_hate",
    }
    TOXICITY_CLASS_RENAME_MAP: Optional[Dict[str, str]] = {
        "severe_toxic": "Severe Toxicity",
        "identity_hate": "Identity Hate",
        "insult": "Insult",
        "obscene": "Obscene",
        "threat": "Threat",
        "toxic": "Toxicity",
        "non_hate": "Non Hate",
    }
    ACCEPTED_CONTENT_WARNING_CLASSES: Optional[Set[str]] = {
        "Violence",
        "Emaciated Bodies",
        "Corpses",
        "Hanging",
        "Air Crash",
        "Explosions And Blasts",
        "Hate Symbols",
        "Nazi Party",
        "White Supremacy",
        "Extremist",
    }

    # Integrations
    ## Telegram
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str

    # Misc
    DEBUG_MOCK_CLASSIFY: bool = False

    class Config:
        env_file = ".env.prod"


@lru_cache()
def get_settings():
    return Settings()
