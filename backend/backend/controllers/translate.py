from pydantic import validate_arguments

from backend.dependencies.aws_ml import get_translate_client


@validate_arguments
def translate_text(
    text: str, source_language: str = "auto", target_language: str = "en"
) -> str:
    client = get_translate_client()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
