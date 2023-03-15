from fastapi import APIRouter, UploadFile, File
from backend.models.models import *
from backend.controllers.upload import *
from backend.controllers.predict_text import *

router = APIRouter()

@router.get("/")
def ping():
    return {"message": "Hello World"}

@router.post("/text")
def submit_text(text: Text):
    #call predict_text.py
    return test_text(text.text)

@router.post("/video")
def submit_video(file: UploadFile=File(...)):
    upload_file_by_content(file.file,'bymfdata',file.filename)
    #call predict_video.py
    return {"file_name": file.filename}