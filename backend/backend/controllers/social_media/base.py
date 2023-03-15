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
