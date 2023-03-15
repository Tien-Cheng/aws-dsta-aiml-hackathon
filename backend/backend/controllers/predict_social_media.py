import logging
import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import validate_arguments

from backend.models.models import SocialMediaPostModel

from .social_media import social_media_integrator_factory

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
            pass
            # If audio or video, attempt to get transcript
            # TODO
            # If image, attempt to get text
            # TODO
            # if media.blob is not None:
            #     combined_text += media.blob
            #     combined_text += " "

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

    # Call prediction function
    # TODO

    # Return prediction
