from fastapi import APIRouter, Depends, File, Form, UploadFile

from backend.controllers.predict_audio import predict_audio
from backend.controllers.predict_social_media import predict_from_social_media_post
from backend.controllers.predict_text import predict_text
from backend.controllers.predict_video import predict_video
from backend.controllers.predict_image import predict_image, moderate_image
from backend.controllers.upload import upload_file_by_content
from backend.dependencies.utils import convert_bytes_to_b64_src
from backend.models.models import PredictionResponseModel
from backend.settings import Settings, get_settings

router = APIRouter(
    prefix="/predict",
)


@router.post("/text", response_model=PredictionResponseModel)
def submit_text(text: str = Form(), settings: Settings = Depends(get_settings)):
    text_pred = predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)
    return PredictionResponseModel(toxicity_predictions=text_pred, content_warnings=[])


@router.post("/url", response_model=PredictionResponseModel)
async def submit_url(url: str = Form(), settings: Settings = Depends(get_settings)):
    text, post = await predict_from_social_media_post(url)
    text_pred = predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)
    content_warnings = []
    if post.media is not None:
        for media in post.media:
            if media.file_type is None:
                continue
            file_type = media.file_type.split("/")[0]
            if file_type == "image":
                if not media.blob:
                    # TODO: get image from s3
                    continue
                encoded_image = convert_bytes_to_b64_src(
                    media.blob, media.file_type or "image/jpeg"
                )
                # Note that we already got the text from the image, so we don't need to
                # call predict_image here
                # Call moderation
                s3_path = media.s3_path.lstrip("s3://")
                bucket, key = s3_path.split("/", 1)
                moderation_labels = moderate_image(key, bucket)
                content_warnings.append(
                    {"blob": encoded_image, "classes": moderation_labels}
                )
    return PredictionResponseModel(toxicity_predictions=text_pred, content_warnings=content_warnings)


@router.post("/image", response_model=PredictionResponseModel)
def submit_image(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    encoded_image = convert_bytes_to_b64_src(
        file.file.read(), file.content_type or "image/jpeg"
    )
    file.file.seek(0)
    upload_file_by_content(file.file, settings.S3_BUCKET_NAME, file.filename)
    text = predict_image(
        file.filename, settings.S3_BUCKET_NAME
    )
    toxic_predict = predict_text(
        text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT
    )
    moderation_labels = moderate_image(
        file.filename, settings.S3_BUCKET_NAME
    )
    return PredictionResponseModel(
        toxicity_predictions=toxic_predict,
        content_warnings=[{"blob": encoded_image, "classes": moderation_labels}],
    )


@router.post("/video", response_model=PredictionResponseModel)
def submit_video(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    upload_file_by_content(file.file, settings.S3_BUCKET_NAME, file.filename)
    text = predict_video(
        file.filename, settings.S3_BUCKET_NAME, settings.VIDEO_REKOGNITION_TIMEOUT
    )
    text_pred = predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)
    return PredictionResponseModel(toxicity_predictions=text_pred, content_warnings=[])


@router.post("/audio", response_model=PredictionResponseModel)
def submit_audio(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    upload_file_by_content(file.file, settings.S3_BUCKET_NAME, file.filename)
    text = predict_audio(
        file.filename, settings.S3_BUCKET_NAME, settings.VIDEO_REKOGNITION_TIMEOUT
    )
    text_pred = predict_text(text, settings.SEGMENT_CHUNK_SIZE, settings.TEXT_ENDPOINT)
    return PredictionResponseModel(toxicity_predictions=text_pred, content_warnings=[])
