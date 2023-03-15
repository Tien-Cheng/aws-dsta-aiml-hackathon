import logging
from time import sleep
from json import dumps
from typing import Dict, List

from botocore.exceptions import ClientError
from pydantic import validate_arguments

from backend.dependencies.comprehend import get_comprehend_client

logger = logging.getLogger(__name__)


@validate_arguments
def segment_text(text: str, span: int) -> List[str]:
    text = text.split(" ")
    return [" ".join(text[i : i + span]) for i in range(0, len(text), span)]


@validate_arguments
def predict_text(chunk: str, chunk_size: int, endpoint: str) -> List[Dict]:
    if len(chunk) == 0:
        return []
    comprehend = get_comprehend_client()
    segments = segment_text(chunk, chunk_size)
    result = []
    logger.info("Sending %s segments to Comprehend", len(segments))
    for chunk in segments:
        attempts = 0
        while True:
            try:
                response = comprehend.classify_document(Text=chunk, EndpointArn=endpoint)
                break
            except ClientError as err:
                attempts += 1
                logger.info("Being rate limited by Comprehend")
                logger.info("Sleeping for 5 seconds")
                sleep(5)
                if attempts > 3:
                    logger.error("Failed to classify text: %s", str(err))
                    raise err
        result.append({"text": chunk, "classes": response["Labels"]})
    logger.info("Predicted: %s", dumps(result))
    return result
