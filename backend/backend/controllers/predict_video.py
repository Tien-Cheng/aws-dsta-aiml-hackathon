from time import sleep

import boto3
from fastapi import status
from fastapi.exceptions import HTTPException

from backend.dependencies.rekognition import get_rekognition_client


def predict_video(filename: str, bucket: str, timeout: int = 3600) -> str:
    rekognition = get_rekognition_client()
    job_details = rekognition.start_text_detection(
        Video={
            "S3Object": {
                "Bucket": bucket,
                "Name": filename,
            }
        }
    )
    job_id = job_details["JobId"]
    detections = rekognition.get_text_detection(JobId=job_id)
    time_elapsed = 0
    while detections["JobStatus"] == "IN_PROGRESS":
        if time_elapsed > timeout:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Timeout while waiting for video text detection",
            )
        sleep(2)
        time_elapsed += 2
        detections = rekognition.get_text_detection(JobId=job_id)
    result = ""
    for text_det in detections["TextDetections"]:
        text = text_det["TextDetection"]["DetectedText"]
        result += text
    return result
