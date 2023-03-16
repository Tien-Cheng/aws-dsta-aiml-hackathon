from youtube_transcript_api import YouTubeTranscriptApi
import os

#from .base import SocialMediaIntegrator

class YoutubeIntegrator():
    def __init__(self, vidurl):
        self.vidurl = vidurl

    def get_transcript(self):
        output = []

        txt = YouTubeTranscriptApi.get_transcript(self.vidurl)
        
        try:
            if os.path.exists("output.txt"):
                os.remove("output.txt")
        
            for i in txt:
                outtxt = (i['text'])
                output.append(outtxt)
                
                with open("output.txt", "a") as opf:
                    opf.write(outtxt + "\n")
                    
        except Exception as error:
            print(error)
            print("SUBTITLES CANNOT BE RETRIEVED")
                
yt = YoutubeIntegrator("rTWM5WuPhlQ")
yt.get_transcript()

