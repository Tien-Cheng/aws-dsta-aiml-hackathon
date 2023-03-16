from urllib.parse import urlparse

from youtube_transcript_api import YouTubeTranscriptApi

from backend.models.models import SocialMediaPostModel

from .base import SocialMediaIntegrator


class YoutubeIntegrator(SocialMediaIntegrator):
    def __init__(self):
        super().__init__()

    async def get_post_by_url(self, post_url: str) -> SocialMediaPostModel:
        # From a youtube video url, get the ID
        # https://www.youtube.com/watch?v=9bZkp7q19f0
        # or https://youtu.be/9bZkp7q19f0
        self.logger.info("Getting youtube post: %s", post_url)
        parsed_url = urlparse(post_url)
        # check query params
        if parsed_url.query:
            self.logger.info("1")
            video_id = parsed_url.query.split("=")[1]
        else:
            self.logger.info("2")
            video_id = parsed_url.path.split("/")[-1]
        self.logger.info("Youtube video id: %s", video_id)
        text = ""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            for line in transcript:
                text += line["text"] + " "
        except Exception as error:
            text = "SUBTITLES CANNOT BE RETRIEVED"
            self.logger.error("Error getting youtube subtitles: %s", error)

        return SocialMediaPostModel(
            text=text,
            post_id=video_id,
            post_url=post_url,
        )
