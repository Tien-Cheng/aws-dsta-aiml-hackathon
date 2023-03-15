from datetime import datetime
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel


class InputModel(BaseModel):
    # e.g post text, video description, etc.
    text: Optional[str] = None
    # e.g youtube video title
    title: Optional[str] = None
    # s3 paths to the media
    media_paths: Optional[List[str]] = None


class SocialMediaPostModel(InputModel):
    # unique id of the post
    post_id: str
    # url of the post
    post_url: AnyHttpUrl
    # When the post was created
    timestamp: Optional[datetime] = None
    # unique id of the poster
    poster_id: Optional[str] = None
    # e.g channel title etc
    poster_name: Optional[str] = None
    # any responses to the original post
    # e.g comments, replies, etc
    children: Optional[List["SocialMediaPostModel"]] = None


class PredictionResponse(BaseModel):
    # TODO
    pass
