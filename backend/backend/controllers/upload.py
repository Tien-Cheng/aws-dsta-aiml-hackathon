import io
import logging
import os
from typing import Union

from botocore.exceptions import ClientError
from pydantic import validate_arguments

from backend.dependencies.storage import get_s3_client

logger = logging.getLogger(__name__)


@validate_arguments
def upload_file_by_path(file_name: str, bucket: str, object_name=None) -> bool:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as err:
        logger.error(err)
        return False
    return True


#@validate_arguments
def upload_file_by_content(
    file_content: Union[bytes, io.BytesIO], bucket: str, object_name: str
) -> bool:
    """Upload a file to an S3 bucket

    :param file_content: File content to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = get_s3_client()
    try:
        s3_client.upload_fileobj(file_content, bucket, object_name)
    except ClientError as err:
        logger.error(err)
        return False
    return True
