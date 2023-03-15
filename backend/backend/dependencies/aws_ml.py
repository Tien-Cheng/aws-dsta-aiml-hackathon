from functools import lru_cache

import boto3
from botocore.config import Config

from backend.settings import get_settings

settings = get_settings()

BOTO_CONFIG = Config(
    retries={"max_attempts": settings.API_RETRY_ATTEMPTS, "mode": "standard"}
)


@lru_cache()
def get_comprehend_client():
    return boto3.client(
        "comprehend",
        config=BOTO_CONFIG,
    )


@lru_cache()
def get_rekognition_client():
    return boto3.client(
        "rekognition",
        config=BOTO_CONFIG,
    )


@lru_cache()
def get_transcribe_client():
    return boto3.client(
        "transcribe",
        config=BOTO_CONFIG,
    )


@lru_cache()
def get_translate_client():
    return boto3.client(
        "translate",
        config=BOTO_CONFIG,
    )
