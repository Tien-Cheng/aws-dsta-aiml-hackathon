from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import get_settings
from .routers.router import router
from .dependencies.storage import init_bucket

app = FastAPI()
settings = get_settings()

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the router to the app
app.include_router(router)

# Add startup events
# Initialize S3 bucket
app.add_event_handler("startup", init_bucket)
