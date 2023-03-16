from .base import SocialMediaIntegrator
from .telegram import TelegramIntegrator
from .youtube import YoutubeIntegrator


class SocialMediaIntegratorFactory:
    def __init__(self):
        self.integrators = {
            "telegram": TelegramIntegrator,
            "youtube" : YoutubeIntegrator
        }
        self.active_integrators = {}

    def get_integrator(
        self, social_media: str, *args, **kwargs
    ) -> SocialMediaIntegrator:
        if social_media not in self.integrators:
            raise ValueError(f"Invalid social media: {social_media}")
        if social_media not in self.active_integrators:
            self.active_integrators[social_media] = self.integrators[social_media](
                *args, **kwargs
            )
        return self.active_integrators[social_media]


# Create a singleton instance of the factory
social_media_integrator_factory = SocialMediaIntegratorFactory()
