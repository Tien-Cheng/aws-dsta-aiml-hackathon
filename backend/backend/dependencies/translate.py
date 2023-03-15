from functools import lru_cache

import boto3


@lru_cache()
def get_translate_client():
    return boto3.client("translate")
