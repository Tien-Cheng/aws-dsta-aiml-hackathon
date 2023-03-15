import boto3
import json

def seg_text(text):
    span = 5 #to be specified in settings
    text = text.split(" ")
    return [" ".join(text[i:i+span]) for i in range(0, len(text), span)]

def test_text(text):
    text_list=seg_text(text)
    sentiment_dict={}
    comprehend = boto3.client(service_name='comprehend')
    for i in text_list:
        response=comprehend.detect_sentiment(Text=i, LanguageCode='en')
        sentiment_dict[i]={response['Sentiment']}
    print(sentiment_dict)
    return sentiment_dict
