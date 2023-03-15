import logging
from abc import ABC, abstractmethod

from backend.models.models import SocialMediaPostModel


class SocialMediaIntegrator(ABC):
    """Abstract class to denote
    common methods for social media data integrators
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    async def get_post_by_url(self, post_url: str) -> SocialMediaPostModel:
        """Get post by url"""
        pass

    @abstractmethod
    async def save_media_to_s3(
        self, post: SocialMediaPostModel
    ) -> SocialMediaPostModel:
        """Save media to s3

        This should attempt to download any media
        associated with the post and save it to s3.
        """
        pass
