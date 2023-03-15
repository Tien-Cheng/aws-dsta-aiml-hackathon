from functools import lru_cache

import boto3


@lru_cache()
def get_comprehend_client():
    return boto3.client("comprehend")
