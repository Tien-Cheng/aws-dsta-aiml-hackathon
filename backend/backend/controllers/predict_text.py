import boto3
import json

def test_text(text):
    comprehend = boto3.client(service_name='comprehend')
    return(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    