import boto3
import time

def predict_video(vid):

    rekognition=boto3.client('rekognition')

  
    startTextDetection=rekognition.start_text_detection(Video={'S3Object': {'Bucket': 'bymfdata','Name': vid,}})
    textJobId = startTextDetection['JobId']
    getTextDetection = rekognition.get_text_detection(JobId=textJobId)

    while(getTextDetection['JobStatus'] == 'IN_PROGRESS'):
        time.sleep(2)
    
        getTextDetection = rekognition.get_text_detection(JobId=textJobId)
    

                        
    response=getTextDetection
    result=""
    for textDetection in response['TextDetections']:
        text=textDetection['TextDetection']["DetectedText"]
        result+=text

    return result