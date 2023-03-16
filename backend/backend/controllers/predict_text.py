import logging
from json import dumps
from typing import Dict, List

from pydantic import validate_arguments

from backend.dependencies.aws_ml import get_comprehend_client
from backend.settings import get_settings

from .translate import translate_text

logger = logging.getLogger(__name__)
settings = get_settings()


@validate_arguments
def segment_text(text: str, span: int) -> List[str]:
    text = text.split(" ")
    return [" ".join(text[i : i + span]) for i in range(0, len(text), span)]


@validate_arguments
def predict_text(text: str, chunk_size: int, endpoint: str) -> List[Dict]:
    if len(text) == 0:
        return []
    comprehend = get_comprehend_client()
    # Find language
    lang = comprehend.detect_dominant_language(Text=text)
    # Check if english
    if lang["Languages"][0]["LanguageCode"] != "en":
        # Translate to english
        text = translate_text(
            text=text,
            source_language=lang["Languages"][0]["LanguageCode"],
            target_language="en",
        )
    segments = segment_text(text, chunk_size)
    result = []
    logger.info("Sending %s segments to Comprehend", len(segments))
    for chunk in segments:
        # NOTE: Use to avoid rate limit when developing
        if settings.DEBUG_MOCK_CLASSIFY:
            response = {"Labels": [{"Name": "non_hate", "Score": 0.9}]}
        else: 
            response = comprehend.classify_document(Text=chunk, EndpointArn=endpoint)
        result.append({"text": chunk, "classes": response["Labels"]})
    logger.info("Predicted: %s", dumps(result))
    return result
