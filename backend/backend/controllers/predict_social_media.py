import logging
import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import validate_arguments

from backend.models.models import SocialMediaPostModel
from backend.settings import get_settings

from .social_media import social_media_integrator_factory
from .upload import upload_file_by_content
from .predict_audio import predict_audio
from .predict_video import predict_video

logger = logging.getLogger(__name__)


@validate_arguments
def get_platform_from_url(url: str) -> Optional[str]:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    # Check if url is a telegram url
    if re.search(r"(?:www\.)?t\.me", domain):
        return "telegram"

    # Check if url is a YouTube url
    if re.search(r"(?:www\.)?(?:youtube\.com|youtu\.be)", domain):
        return "youtube"

    # No platform found
    return None


@validate_arguments
def extract_information_from_post(post: SocialMediaPostModel) -> str:
    combined_text = ""

    if post.text:
        combined_text += post.text
        combined_text += " "

    if post.title:
        combined_text += post.title
        combined_text += " "

    if post.media is not None:
        for media in post.media:
            # If audio or video, attempt to get transcript
            if not media.file_type:
                continue
            if not media.s3_path:
                if not media.blob:
                    continue
                else:
                    settings = get_settings()
                    upload_file_by_content(
                        media.blob, settings.S3_BUCKET_NAME, media.file_name
                    )
                    bucket, key = settings.S3_BUCKET_NAME, media.file_name
            else:
                # get file location from s3 path
                s3_path = media.s3_path.lstrip("s3://")
                # s3_path will be something like "s3://bucket/path/to/file"
                bucket, key = s3_path.split("/", 1)
                # file type will be something like "audio/mp4"
            file_type = media.file_type.split("/")[0]
            if file_type == "audio":
                combined_text += predict_audio(key, bucket)
                combined_text += " "
            elif file_type == "video":
                combined_text += predict_video(key, bucket)
                combined_text += " "
            elif file_type == "image":
                # TODO
                continue

    # Recursively get text from children
    # Base case is when post.children is None
    if post.children is not None:
        for child in post.children:
            combined_text += extract_information_from_post(child)

    return combined_text


@validate_arguments
async def predict_from_social_media_post(url: str, platform: Optional[str] = None):
    # Remove query parameters from url
    url = url.split("?")[0]
    # Attempt to figure out the platform from the url
    if platform is None:
        platform = get_platform_from_url(url)
        if platform is None:
            raise ValueError("Could not determine platform from url")

    # Initialize the integrator
    integrator = social_media_integrator_factory.get_integrator(platform)

    # Get the post
    post = await integrator.get_post_by_url(url)

    # Extract text from the post to be used for prediction
    text = extract_information_from_post(post)
    logger.info(f"Extracted text: {text}")
    return text
