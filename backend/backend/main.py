from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.router import router

app = FastAPI()

# Add CORS middleware to allow requests from frontend
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the router to the app
app.include_router(router)