import logging
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from backend.settings import get_settings

logger = logging.getLogger(__name__)


@lru_cache()
def get_s3_client():
    return boto3.client("s3")


def init_bucket() -> bool:
    settings = get_settings()
    s3_client = get_s3_client()

    try:
        s3_client.create_bucket(Bucket=settings.S3_BUCKET_NAME)
    except ClientError as err:
        logging.error(err)
        return False
    return True
