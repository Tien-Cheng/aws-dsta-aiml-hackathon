import logging
from json import dumps
from typing import Dict, List

from pydantic import validate_arguments

from backend.dependencies.comprehend import get_comprehend_client

logger = logging.getLogger(__name__)


@validate_arguments
def segment_text(text: str, span: int) -> List[str]:
    text = text.split(" ")
    return [" ".join(text[i : i + span]) for i in range(0, len(text), span)]


@validate_arguments
def predict_text(chunk: str, chunk_size: int, endpoint: str) -> List[Dict]:
    comprehend = get_comprehend_client()
    segments = segment_text(chunk, chunk_size)
    result = []
    for chunk in segments:
        response = comprehend.classify_document(Text=chunk, EndpointArn=endpoint)
        result.append({"text": chunk, "classes": response["Labels"]})
    logger.info("Predicted: %s", dumps(result))
    return result
