import logging
from base64 import b64encode
from mimetypes import guess_extension
from tempfile import NamedTemporaryFile
from typing import List, Optional, Set

from pyffmpeg import FFmpeg

logger = logging.getLogger(__name__)


def convert_bytes_to_b64_src(blob: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{b64encode(blob).decode('utf-8')}"


def get_thumbnail_b64_src(video_bytes: bytes, mime_type: str) -> str:
    try:
        suffix = guess_extension(mime_type)
        with NamedTemporaryFile(suffix=suffix) as tmp:
            with NamedTemporaryFile(suffix=".jpg") as thumb:
                tmp.write(video_bytes)
                tmp.seek(0)
                ffmpeg = FFmpeg()
                # ffmpeg.convert(
                #     tmp.name,
                #     thumb.name,
                # )
                ffmpeg.options(
                    f"-i {tmp.name} -ss 00:00:01.000 -vframes 1 {thumb.name}"
                )
                # Read thumbnail to bytes
                with open(thumb.name, "rb") as f:
                    return convert_bytes_to_b64_src(f.read(), "image/jpeg")
    except Exception as err:
        logger.error(f"Error getting thumbnail: {err}")
        return ""


def filter_predictions(
    predictions: List[dict],
    confidence_threshold: float = 0.5,
    accepted_classnames: Optional[Set[str]] = None,
    rename_classes: Optional[dict] = None,
) -> List[dict]:
    print(f"Predictions: {predictions}")
    for prediction in predictions:
        filtered_classes = []
        for class_ in prediction["classes"]:
            print(class_)
            if class_["Score"] >= confidence_threshold and (
                accepted_classnames is None or class_["Name"] in accepted_classnames
            ):
                print("Above threshold")
                if rename_classes is not None and class_["Name"] in rename_classes:
                    class_["Name"] = rename_classes[class_["Name"]]
                filtered_classes.append(class_)
        # update prediction with filtered classes
        prediction["classes"] = filtered_classes
    return predictions
