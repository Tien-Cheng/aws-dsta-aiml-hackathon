import logging
from json import loads
from tempfile import NamedTemporaryFile
from time import sleep
from uuid import uuid4

from fastapi import status
from fastapi.exceptions import HTTPException

from backend.dependencies.aws_ml import (get_rekognition_client)

logger = logging.getLogger(__name__)


def predict_image(filename: str, bucket: str) -> str:
    rekognition = get_rekognition_client()

    #Text Detection
    detections= rekognition.detect_text(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": filename,
            }
        }
    )
    
    result=""
    
    result += "DETECTED TEXT (OCR): "
    for text_det in detections["TextDetections"]:
        text = text_det["DetectedText"]
        result += text + " "
    logger.info("OCR job succeeded")

    print(result)
    return result


def moderate_image(filename: str, bucket: str) -> dict:
    rekognition = get_rekognition_client()
    #Content Moderation
    moderations= rekognition.detect_moderation_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": filename,
            }
        }
    )
    results = []
    for label in moderations["ModerationLabels"]:
        results.append({
            "Name": label["Name"],
            "Score": label["Confidence"],
        })
    return results

