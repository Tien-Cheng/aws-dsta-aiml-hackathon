from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile

from backend.controllers.predict_social_media import predict_from_social_media_post
from backend.controllers.predict_text import predict_text
from backend.controllers.upload import upload_file_by_content
from backend.models.models import PredictionResponseModel
from backend.settings import Settings, get_settings

router = APIRouter(
    prefix="/predict",
)


@router.post("/text", response_model=List[PredictionResponseModel])
def submit_text(text: str = Form(), settings: Settings = Depends(get_settings)):
    return predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)


@router.post("/url", response_model=List[PredictionResponseModel])
async def predict_from_url(
    url: str = Form(), settings: Settings = Depends(get_settings)
):
    text = await predict_from_social_media_post(url)
    return predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)


@router.post("/video", response_model=List[PredictionResponseModel])
def submit_video(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    upload_file_by_content(file.file, settings.S3_BUCKET_NAME, file.filename)
    # call predict_video.py
    return {"file_name": file.filename}
