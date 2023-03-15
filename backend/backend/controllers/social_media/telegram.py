from mimetypes import guess_extension
from os import remove
from os.path import basename
from tempfile import NamedTemporaryFile

from fastapi import status
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from fastapi.exceptions import HTTPException

from backend.controllers.upload import upload_file_by_path
from backend.models.models import MediaModel, SocialMediaPostModel
from backend.settings import get_settings

from .base import SocialMediaIntegrator


class TelegramIntegrator(SocialMediaIntegrator):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.telegram_api_key = self.settings.TELEGRAM_API_ID
        self.telegram_api_hash = self.settings.TELEGRAM_API_HASH
        self.client = TelegramClient(
            "anon", self.telegram_api_key, self.telegram_api_hash
        )

    async def get_2fa_code(self, phone_number: str) -> bool:
        await self.client.connect()
        sent = await self.client.send_code_request(phone_number)
        return sent

    async def sign_in(self, phone_number: str, code: str):
        await self.client.connect()
        await self.client.sign_in(phone=phone_number, code=code)

    async def sign_out(self):
        # delete session file
        await self.client.disconnect()
        remove("anon.session")

    async def get_post_by_url(
        self, post_url: str, save_s3: bool = True, save_blob: bool = False
    ) -> SocialMediaPostModel:
        # id: channel_id/post_id
        # note that it should be stripped of any domain
        # telegram post urls are in the format
        # https://t.me/c/1234567890/1234567890
        # so we can just split on the last /
        # TODO: validate url
        post_id = post_url.split("/")[-1]
        channel_id = post_url.split("/")[-2]
        self.logger.info("Post id: %s", post_id)
        self.logger.info("Channel id: %s", channel_id)

        # get post
        self.logger.info("Starting telegram client")
        async with self.client:
            # self.logger.info("Getting post from: %s", post_url)
            await self.client.get_dialogs()
            try:
                post: Message = await self.client.get_messages(
                    channel_id, ids=int(post_id)
                )
            except ValueError as err:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {post_id} in channel with id {channel_id} not found",
                ) from err
            self.logger.info("Retrieved post")

            # Get metadata
            timestamp = post.date
            post_id = post.id
            poster_id = post.from_id
            if poster_id:
                # Not sure if this is the id of the channel or the user
                poster_id = poster_id.chat_id
            poster_name = post.post_author

            # Get content
            text = post.message
            media = post.media
            title = None
            self.logger.info("Text: %s", text or "")

            if media and post.file:
                self.logger.info("Attempting to download media")
                data = None
                if post.file.mime_type:
                    suffix = guess_extension(post.file.mime_type)
                elif post.file.name:
                    suffix = "." + post.file.name.split(".")[-1].strip(".")
                else:
                    suffix = None
                with NamedTemporaryFile(suffix=suffix) as f:
                    await self.client.download_media(post, file=f.name)
                    self.logger.info("Downloaded media")
                    filename = post.file.name or basename(f.name)
                    if save_s3:
                        # Attempt to save to s3
                        s3_path = f"s3://{self.settings.S3_BUCKET_NAME}/{filename}"
                        if upload_file_by_path(
                            f.name, self.settings.S3_BUCKET_NAME, filename
                        ):
                            self.logger.info(
                                "Successfully uploaded file to s3: %s", s3_path
                            )
                        else:
                            self.logger.error(
                                "Failed to upload file to s3: %s", s3_path
                            )
                            s3_path = None
                    if save_blob:
                        data = f.file.read()
                media = MediaModel(
                    file_name=filename,
                    file_type=post.file.mime_type,
                    s3_path=s3_path,
                    blob=data,
                )

            post_data = SocialMediaPostModel(
                post_id=post_id,
                post_url=post_url,
                timestamp=timestamp,
                poster_id=poster_id,
                poster_name=poster_name,
                text=text,
                title=title,
                media=[media] if media else None,
            )
            # await self.client.disconnect()
            self.logger.info("Task complete")

        return post_data
