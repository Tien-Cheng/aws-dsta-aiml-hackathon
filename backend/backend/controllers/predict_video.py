import logging
from json import loads
from tempfile import NamedTemporaryFile
from time import sleep
from typing import List, Tuple
from uuid import uuid4

from fastapi import status
from fastapi.exceptions import HTTPException

from backend.dependencies.aws_ml import (get_rekognition_client,
                                         get_transcribe_client)
from backend.dependencies.storage import get_s3_client

logger = logging.getLogger(__name__)


def content_moderation_video(
    filename: str, bucket: str, timeout: int = 3600
) -> List[dict]:
    rekognition = get_rekognition_client()
    # Content Moderation
    moderations = rekognition.start_content_moderation(
        Video={
            "S3Object": {
                "Bucket": bucket,
                "Name": filename,
            }
        }
    )
    job_id = moderations["JobId"]
    logger.info("Content moderation job started")
    # Wait for job to finish
    time_elapsed = 0
    while True:
        sleep(5)
        time_elapsed += 5
        if time_elapsed > timeout:
            logger.error("Content moderation job timed out")
            break
        job_status = rekognition.get_content_moderation(
            JobId=job_id,
            SortBy="TIMESTAMP",
        )
        if job_status["JobStatus"] == "IN_PROGRESS":
            continue
        elif job_status["JobStatus"] == "SUCCEEDED":
            break
        else:
            logger.error("Content moderation job failed")
            break

    results = []
    seen_labels = set()
    for det in job_status["ModerationLabels"]:
        label = det["ModerationLabel"]
        name = label["Name"]
        if name in seen_labels:
            continue
        seen_labels.add(name)
        results.append(
            {
                "Name": name,
                "Score": label["Confidence"],
            }
        )
    return results


def predict_video(filename: str, bucket: str, timeout: int = 3600) -> str:
    rekognition = get_rekognition_client()
    transcribe = get_transcribe_client()
    # Perform OCR on video
    ocr_job_details = rekognition.start_text_detection(
        Video={
            "S3Object": {
                "Bucket": bucket,
                "Name": filename,
            }
        }
    )
    ocr_job_id = ocr_job_details["JobId"]

    # Transcribe the video
    transcript_name = str(uuid4())[:8]
    transcript_job_details = transcribe.start_transcription_job(
        TranscriptionJobName=transcript_name,
        Media={
            "MediaFileUri": f"s3://{bucket}/{filename}",
        },
        OutputBucketName=bucket,
        OutputKey=f"{transcript_name}.txt",
        IdentifyLanguage=True,
    )
    transcription_job_id = transcript_job_details["TranscriptionJob"][
        "TranscriptionJobName"
    ]
    transcript = transcribe.get_transcription_job(
        TranscriptionJobName=transcription_job_id
    )
    detections = rekognition.get_text_detection(JobId=ocr_job_id)
    time_elapsed = 0
    transcribe_done = False
    detect_done = False
    while not (transcribe_done and detect_done):
        if time_elapsed > timeout:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Timeout while waiting for video transcription",
            )
        sleep(2)
        time_elapsed += 2
        if not transcribe_done:
            transcript = transcribe.get_transcription_job(
                TranscriptionJobName=transcription_job_id
            )
            if (
                transcript["TranscriptionJob"]["TranscriptionJobStatus"]
                != "IN_PROGRESS"
            ):
                transcribe_done = True
        if not detect_done:
            detections = rekognition.get_text_detection(JobId=ocr_job_id)
            if detections["JobStatus"] != "IN_PROGRESS":
                detect_done = True

    result = ""
    # Process transcript
    s3_client = get_s3_client()
    if transcript["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        with NamedTemporaryFile() as tmp:
            s3_client.download_fileobj(bucket, f"{transcript_name}.txt", tmp)
            tmp.seek(0)
            transcription_json = tmp.read().decode("utf-8")
            transcripts = loads(transcription_json)["results"]["transcripts"]
            result += "TRANSCRIPT: "
            for transcript in transcripts:
                result += transcript["transcript"] + " "
        logger.info("Transcription job succeeded")
    else:
        logger.error("Transcription job failed")
    #   raise HTTPException(
    #       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #       detail="Transcription job failed",
    #   )

    if detections["JobStatus"] == "SUCCEEDED":
        result += "DETECTED TEXT (OCR): "
        for text_det in detections["TextDetections"]:
            text = text_det["TextDetection"]["DetectedText"]
            result += text + " "
        logger.info("OCR job succeeded")
    else:
        logger.error("OCR job failed")
    #   raise HTTPException(
    #       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #       detail="OCR job failed",
    #   )

    return result
