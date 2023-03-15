import shutil
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.models.models import *
from backend.controllers.upload import *
from backend.controllers.predict_text import *

router = APIRouter()

frontend = Jinja2Templates(directory="..\\frontend\\public")

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return frontend.TemplateResponse("index.html", {"request": request})

@router.post("/text")
def submit_text(text: Text):
    #call predict_text.py
    return test_text(text.text)

@router.post("/video")
def submit_video(file: UploadFile=File(...)):
    upload_file_by_content(file.file,'bymfdata',file.filename)
    #call predict_video.py
    return {"file_name": file.filename}