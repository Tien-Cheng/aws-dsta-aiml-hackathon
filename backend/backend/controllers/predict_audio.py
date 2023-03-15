from json import loads
from tempfile import NamedTemporaryFile
from time import sleep
from uuid import uuid4

from fastapi import status
from fastapi.exceptions import HTTPException

from backend.dependencies.aws_ml import get_transcribe_client
from backend.dependencies.storage import get_s3_client


def predict_audio(filename: str, bucket: str, timeout: int = 3600) -> str:
    transcribe = get_transcribe_client()
    # Transcribe the audio file
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
    time_elapsed = 0
    transcribe_done = False
    while not transcribe_done:
        if time_elapsed > timeout:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Timeout while waiting for audio transcription",
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
    result = "TRANSCRIPT:"
    # Process transcript
    s3_client = get_s3_client()
    with NamedTemporaryFile() as tmp:
        s3_client.download_fileobj(bucket, f"{transcript_name}.txt", tmp)
        tmp.seek(0)
        transcription_json = tmp.read().decode("utf-8")
        transcripts = loads(transcription_json)["results"]["transcripts"]
        for transcript in transcripts:
            result += transcript["transcript"] + " "
    return result
