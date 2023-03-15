import boto3
import json

def seg_text(text):
    span = 5 #to be specified in settings
    text = text.split(" ")
    return [" ".join(text[i:i+span]) for i in range(0, len(text), span)]

def test_text(text):
    text_list=seg_text(text)
    result=[]
    comprehend = boto3.client(service_name='comprehend')
    endpointarn="arn:aws:comprehend:us-east-1:087582090241:document-classifier-endpoint/toxic-comments-endpoint"
    for i in text_list:
        response=comprehend.classify_document(Text=i, EndpointArn=endpointarn)
        result.append({"text":i, "classes":response["Labels"]})

    print(result)
    return result
