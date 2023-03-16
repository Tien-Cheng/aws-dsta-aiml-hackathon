import logging

# Make logging work with uvicorn
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies.storage import init_bucket
from .routers.predict import router as predict_router
from .routers.telegram import router as telegram_router
from .settings import get_settings

app = FastAPI()
settings = get_settings()
routers = [
    predict_router,
    telegram_router,
]

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add startup events
# Initialize S3 bucket
app.add_event_handler("startup", init_bucket)

# Add the router to the app
for router in routers:
    app.include_router(router)


@app.get("/")
def ping():
    return {"message": "Hello World"}
