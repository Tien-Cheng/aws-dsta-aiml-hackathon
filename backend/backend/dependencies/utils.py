from base64 import b64encode
from typing import List, Optional, Set


def convert_bytes_to_b64_src(blob: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{b64encode(blob).decode('utf-8')}"


def filter_predictions(
    predictions: List[dict],
    confidence_threshold: float = 0.5,
    accepted_classnames: Optional[Set[str]] = None,
    rename_classes: Optional[dict] = None,
) -> List[dict]:
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
